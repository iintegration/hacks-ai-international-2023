import os
import re
from collections import defaultdict
from pathlib import Path
from typing import TypedDict

import torch
from chromadb.config import Settings
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from llama_cpp import Llama

from app.background import first_model

EMBEDDER_ID = "ai-forever/sbert_large_nlu_ru"
SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь c людьми и помогаешь им."
SYSTEM_TOKEN = 1587
USER_TOKEN = 2188
BOT_TOKEN = 12435
LINEBREAK_TOKEN = 13
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDER_ID)
n_ctx = 3000
top_k = 40
top_p = 0.5
temperature = 0.05
repeat_penalty = 1.1
model_path = "/cache/saiga/model-q4_K.gguf"


ROLE_TOKENS = {"user": USER_TOKEN, "bot": BOT_TOKEN, "system": SYSTEM_TOKEN}


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    return get_message_tokens(model, **system_message)


def chat_saiga(message, model):
    system_tokens = get_system_tokens(model)
    tokens = system_tokens

    message_tokens = get_message_tokens(
        model=model, role="user", content=message
    )
    role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
    tokens += message_tokens + role_tokens
    generator = model.generate(
        tokens,
        top_k=top_k,
        top_p=top_p,
        temp=temperature,
        repeat_penalty=repeat_penalty,
        reset=True,
    )

    result_list = []
    for token in generator:
        token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
        tokens.append(token)
        if token == model.token_eos():
            break
        result_list.append(token_str)
    return "".join(result_list)


def sliding_window(lst, window_size, step_size):
    windows = []
    for i in range(0, len(lst) - window_size + 1, step_size):
        windows.append(lst[i : i + window_size])
    return windows


def build_index_time(full_text, chunk_size, chunk_overlap):
    """База текстовых батчей на основе таймкодов транскрибатора."""
    documents = []
    for chunk in sliding_window(
        full_text["chunks"], chunk_size, chunk_overlap
    ):
        meta_data = (chunk[0]["timestamp"][0], chunk[-1]["timestamp"][0])
        chunk_text = " ".join([element["text"] for element in chunk])
        documents.append(
            Document(
                page_content=chunk_text,
                metadata={"start": meta_data[0], "end": meta_data[1]},
            )
        )

    fixed_documents = [doc for doc in documents if doc]
    return Chroma.from_documents(
        fixed_documents,
        embeddings,
        client_settings=Settings(anonymized_telemetry=False),
    )


def retrieve(text, db, k_documents):
    """Поиск ближайших батчей текста."""
    if db:
        retriever = db.as_retriever(search_kwargs={"k": k_documents})
        docs = retriever.get_relevant_documents(text)
        return "\n\n".join([doc.page_content for doc in docs])
    return None


# очистка терминов
def clear_output(output):
    output = (re.sub("""термин|[\\{\\}:\n\r'"]""", "", output)).split()
    if len(output) < 3 and output:
        return " ".join(output)
    return "None"


def first_retrieve(text, db):
    """Вывод ближайшего элемента дб."""
    if db:
        retriever = db.as_retriever(search_kwargs={"k": 1})
        return retriever.get_relevant_documents(text)[0]
    return None


def build_index_big(text, chunk_size, chunk_overlap):
    """База текстовых батчей для конспекта."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    documents = text_splitter.split_documents([Document(page_content=text)])

    fixed_documents = [doc for doc in documents if doc]
    return Chroma.from_documents(
        fixed_documents,
        embeddings,
        client_settings=Settings(anonymized_telemetry=False),
    )


class Result(TypedDict):
    term: str
    definition: str
    start: float
    end: float


def process(full_text: first_model.Result) -> list[Result]:
    print(os.listdir(model_path))
    print(os.listdir(Path(model_path)))
    print(Path(model_path))
    model_s = Llama(model_path=Path(model_path), n_ctx=n_ctx, n_gpu_layers=-1)

    db = build_index_time(full_text, 10, 5)
    # ищем список терминов
    terms_list = []
    for batch in db.get()["documents"]:
        term_prompt = f"""
    Найди ключевой термин для которого дано опеределение в данном тексте.
    Важно: для термина должно быть дано опредление в тексте.
    Если термин c определением есть, выводи {{термин}}
    Если термина c определением нет, то выводи {{None}}.
    Текст:
    {batch}
    """
        with torch.no_grad():
            output = chat_saiga(term_prompt, model_s)
        output = clear_output(output)
        terms_list.append(output)

    terms_list = {t.lower() for t in terms_list}
    terms_list.discard("none")

    terms_dict_list = []
    for t in terms_list:
        terms_dict = defaultdict(str)

        chain_prompt = f"""{t} - это"""
        term_text = retrieve(chain_prompt, db, 5)

        definition_prompt = f"""
    Составь определение термину "{t}" на основе текста
    Вывод должен быть в формате термин - определение
    Дай пожалуйста определение термину {t} -

    Текст
    {term_text}
    """
        meta_time = first_retrieve(chain_prompt, db).metadata

        terms_dict["term"] = t

        with torch.no_grad():
            output = chat_saiga(definition_prompt, model_s)
        output = output[len(t + " - ") :]

        terms_dict["definition"] = output
        terms_dict["start"] = meta_time["start"]
        terms_dict["end"] = meta_time["end"]

        terms_dict_list.append(terms_dict)

    return terms_dict_list

    #
    #
    # for document_id in db.get()["ids"]:
    #     db._collection.delete(ids=document_id)
    # db.persist()
    #
    # db = build_index_big(full_text["text"], 3000, 30)
    #
    # batch_summ = []
    # for batch in db.get()["documents"]:
    #     summ_prompt = f"""
    #     Оставь только важную информацию в данном тексте.
    #     Информацию выводи сплошным текстом
    #     Формат вывода:
    #     Важная информация: {{информация}}
    #
    #
    #     Текст:
    #     {batch}
    #     """
    #     with torch.no_grad():
    #         output = chat_saiga(summ_prompt, model_s)
    #     output = output[len("Важная информация:") :] + "\n"
    #     print(chat_saiga(summ_prompt, model_s).replace("\n", ""))
    #     batch_summ.append(output)
    #     batch_summ = " ".join(batch_summ)
    #
    # for document_id in db.get()["ids"]:
    #     db._collection.delete(ids=document_id)
    # db.persist()
    # torch.cuda.empty_cache()
