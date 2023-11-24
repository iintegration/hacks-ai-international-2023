from dataclasses import asdict
from datetime import timedelta
from http import HTTPStatus
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, HTTPException
from miniopy_async import S3Error

from app.deps import arq, edgedb, minio
from app.models.requests.create_lecture import CreateLecture
from app.models.responses.created_lecture import CreatedLecture
from app.models.responses.lecture import Lecture
from app.models.responses.preview_lecture import PreviewLecture
from app.queries import (
    create_lecture,
    delete_lectures,
    get_lecture,
    get_lectures,
    set_lecture_status,
)
from app.settings import SETTINGS

router = APIRouter(prefix="/lectures")


@router.get("/")
async def all_lectures() -> list[PreviewLecture]:
    lectures = await get_lectures(edgedb.client)
    return [PreviewLecture(**asdict(x)) for x in lectures]


@router.post("/", status_code=HTTPStatus.CREATED)
async def create(lecture: CreateLecture) -> CreatedLecture:
    filename_suffix = Path(lecture.filename).suffix
    created_lecture = await create_lecture(
        edgedb.client, filename=lecture.filename, filename_suffix=filename_suffix
    )

    upload_url = await minio.client.presigned_put_object(
        SETTINGS.s3_bucket,
        object_name=created_lecture.object_name,
        expires=timedelta(minutes=10),
        change_host=SETTINGS.s3_public_host,
    )

    return CreatedLecture(id=created_lecture.id, upload_url=upload_url)


@router.post("/{lecture_id}/start_analyze/")
async def start_analyze(lecture_id: UUID) -> None:
    lecture = await get_lecture(edgedb.client, id=lecture_id)

    if lecture is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Lecture not found"
        )

    if lecture.status.value != "Created":
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Analyze already started"
        )

    try:
        await minio.client.stat_object(
            bucket_name=SETTINGS.s3_bucket, object_name=lecture.object_name
        )
    except S3Error as error:
        raise HTTPException(status_code=404, detail=error.message) from error

    await set_lecture_status(edgedb.client, id=lecture_id, status="Processing")
    await arq.client.enqueue_job(
        "analyze", lecture_id=lecture_id, _job_id=str(lecture_id)
    )


@router.get("/{lecture_id}/")
async def lecture_info(lecture_id: UUID) -> Lecture:
    lecture = await get_lecture(edgedb.client, id=lecture_id)

    if lecture is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Lecture not found"
        )

    if lecture.object_name:
        download_link = minio.client.presigned_get_object(
            bucket_name=SETTINGS.s3_bucket,
            object_name=lecture.object_name,
            expires=timedelta(hours=1),
        )
    else:
        download_link = None

    return Lecture(download_link=download_link, **asdict(lecture))


@router.delete("/")
async def delete_all() -> None:
    await delete_lectures(edgedb.client)
