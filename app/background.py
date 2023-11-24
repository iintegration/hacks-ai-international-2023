import tempfile
from pathlib import Path
from typing import Any
from uuid import UUID

import librosa
import torch
from arq.connections import RedisSettings
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
)

from app.deps import edgedb, minio
from app.queries import finish_analysis, get_lecture
from app.settings import SETTINGS

# openai/whisper-large-v2
TRANSCRIBER_ID = "openai/whisper-large-v2"
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32

processor = AutoProcessor.from_pretrained(TRANSCRIBER_ID)
model_t = AutoModelForSpeechSeq2Seq.from_pretrained(
    TRANSCRIBER_ID,
    torch_dtype=TORCH_DTYPE,
    low_cpu_mem_usage=True,
    use_safetensors=True,
)
model_t.to(DEVICE)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model_t,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=TORCH_DTYPE,
    device=DEVICE,
)


async def analyze(_ctx: dict[str, Any], lecture_id: UUID) -> None:
    lecture = await get_lecture(edgedb.client, id=lecture_id)

    if lecture is None:
        return

    if lecture.object_name is None:
        await finish_analysis(
            edgedb.client,
            lecture_id=lecture_id,
            status="Error",
            text=None,
            error="Lecture doesnt have file",
        )
        return

    # try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = Path(tmpdirname) / lecture.filename
            await minio.client.fget_object(
                bucket_name=SETTINGS.s3_bucket,
                object_name=lecture.object_name,
                file_path=str(file_path),
            )
            audio = librosa.load(str(file_path), sr=16_000)[0]
            result = pipe(audio, generate_kwargs={"language": "russian"})
            await finish_analysis(
                edgedb.client,
                lecture_id=lecture_id,
                status="Processed",
                text=result["text"],
                error=None,
            )
    # except Exception as error:
    #     print(error)
    #     await finish_analysis(
    #         edgedb.client,
    #         lecture_id=lecture_id,
    #         status="Error",
    #         text=None,
    #         error=str(error),
    #     )


async def shutdown(_ctx: dict[str, Any]) -> None:
    await edgedb.client.aclose()


class BackgroundSettings:
    functions = [analyze]
    redis_settings = RedisSettings.from_dsn(
        SETTINGS.redis_dsn.unicode_string()
    )
    on_shutdown = shutdown

    max_jobs = 1
    max_tries = 2
