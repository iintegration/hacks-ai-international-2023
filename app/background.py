import json
from pathlib import Path
from typing import Any
from uuid import UUID

import librosa
import torch
from arq.connections import RedisSettings
from loguru import logger
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
    context_logger = logger.bind(lecture_id=lecture_id)
    context_logger.info("Start")

    lecture = await get_lecture(edgedb.client, id=lecture_id)

    if lecture is None:
        context_logger.warning("No such lecture in database")
        return

    if lecture.filename is None or lecture.object_name is None:
        context_logger.warning("Lecture doesn't have file")
        await finish_analysis(
            edgedb.client,
            lecture_id=lecture_id,
            status="Error",
            text=None,
            error="Lecture without file",
            timestamps=None,
        )
        return

    path = lecture.object_name + lecture.filename
    try:
        context_logger.info("Downloading file")
        await minio.client.fget_object(
            bucket_name=SETTINGS.s3_bucket,
            object_name=lecture.object_name,
            file_path=path,
        )
        context_logger.info("Librosa loading")
        audio = librosa.load(path, sr=16_000)[0]
        context_logger.info("First model processing")
        result = pipe(audio, generate_kwargs={"language": "russian"})
        context_logger.info("First model processing complete")

        await finish_analysis(
            edgedb.client,
            lecture_id=lecture_id,
            status="Processed",
            text=result["text"],
            error=None,
            timestamps=json.dumps(result["chunks"]),
        )
    except Exception as error:
        context_logger.exception("Error")
        await finish_analysis(
            edgedb.client,
            lecture_id=lecture_id,
            status="Error",
            text=None,
            error=repr(error),
            timestamps=None,
        )
    finally:
        Path(path).unlink(missing_ok=True)


async def startup(_ctx: dict[str, Any]) -> None:
    await edgedb.client.ensure_connected()
    await edgedb.client.execute(
        """
        CONFIGURE INSTANCE SET session_idle_timeout :=
            <duration>'5 minutes';
    """
    )
    await edgedb.client.execute(
        """
        CONFIGURE INSTANCE SET session_idle_transaction_timeout :=
            <duration>'5 minutes';
        """
    )


async def shutdown(_ctx: dict[str, Any]) -> None:
    await edgedb.client.aclose()


class BackgroundSettings:
    functions = [analyze]
    redis_settings = RedisSettings.from_dsn(
        SETTINGS.redis_dsn.unicode_string()
    )
    on_startup = startup
    on_shutdown = shutdown

    max_jobs = 1
    max_tries = 2
    job_timeout = 1800
