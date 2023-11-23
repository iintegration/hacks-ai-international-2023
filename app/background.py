import asyncio
import tempfile
from pathlib import Path
from typing import Any
from uuid import UUID

from arq.connections import RedisSettings

from app.deps import edgedb, minio
from app.queries import get_lecture, set_lecture_status
from app.settings import SETTINGS


async def analyze(ctx: dict[str, Any], lecture_id: UUID) -> None:
    lecture = await get_lecture(edgedb.client, id=lecture_id)

    if lecture is None:
        # TODO: some log
        return

    if lecture.object_name is None:
        # TODO: some log if we try to analyze lection without file
        return

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = Path(tmpdirname) / str(lecture_id)
        await minio.client.fget_object(bucket_name=SETTINGS.s3_bucket, object_name=lecture.object_name,
                                       file_path=str(file_path))
        await asyncio.sleep(5)

    await set_lecture_status(edgedb.client, id=lecture_id, status="Processed")


async def shutdown(ctx: dict[str, Any]) -> None:
    await edgedb.client.aclose()


class BackgroundSettings:
    functions = [analyze]
    redis_settings = RedisSettings.from_dsn(SETTINGS.redis_dsn.unicode_string())
    on_shutdown = shutdown

    max_jobs = 1
    max_tries = 2
