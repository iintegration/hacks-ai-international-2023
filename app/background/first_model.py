from typing import TypedDict

import librosa
import torch
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
)

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


class Chunk(TypedDict):
    text: str
    timestamp: tuple[float, float]


class Result(TypedDict):
    text: str
    chunks: list[Chunk]


def process(path: str) -> Result:
    audio = librosa.load(path, sr=16_000)[0]
    return pipe(audio, generate_kwargs={"language": "russian"})
