import json
from pathlib import Path
from typing import Any
from uuid import UUID

from arq.connections import RedisSettings
from loguru import logger

from app.background import first_model, second_model
from app.deps import edgedb, minio
from app.queries import finish_analysis, get_lecture
from app.settings import SETTINGS


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

    path = lecture.object_name
    try:
        context_logger.info("Downloading file")
        await minio.client.fget_object(
            bucket_name=SETTINGS.s3_bucket,
            object_name=lecture.object_name,
            file_path=path,
        )
        context_logger.info("First model processing")
        first_result = first_model.process(path=path)
        context_logger.info("First model processing complete")

        context_logger.info("Second model processing")
        second_result = second_model.process(full_text=first_result)
        context_logger.info("Second model processing complete")
        context_logger.info(second_result)

        await finish_analysis(
            edgedb.client,
            lecture_id=lecture_id,
            status="Processed",
            text=first_result["text"],
            error=None,
            timestamps=json.dumps(first_result["chunks"]),
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
