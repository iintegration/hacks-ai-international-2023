from datetime import timedelta
from http import HTTPStatus
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, HTTPException
from miniopy_async import S3Error
from pydantic import BaseModel

from app.deps import minio, edgedb, arq
from app.queries import create_lecture, get_lecture, set_lecture_status
from app.settings import SETTINGS

router = APIRouter(prefix="/lectures")


class CreateLecture(BaseModel):
    filename: str


class CreatedLecture(BaseModel):
    id: UUID
    upload_url: str


class LectureStatus(BaseModel):
    status: str


@router.post("/", status_code=HTTPStatus.CREATED)
async def create(lecture: CreateLecture) -> CreatedLecture:
    created_lecture = await create_lecture(
        edgedb.client, filename=lecture.filename
    )
    # TODO: класть в базу сразу с суффиксом
    file_suffix = Path(lecture.filename).suffix

    upload_url = await minio.client.presigned_put_object(
        SETTINGS.s3_bucket, str(created_lecture.id) + file_suffix, expires=timedelta(minutes=10)
    )

    return CreatedLecture(id=created_lecture.id, upload_url=upload_url)


@router.post("/{lecture_id}/start_analyze")
async def start_analyze(lecture_id: UUID) -> None:
    lecture = await get_lecture(edgedb.client, id=lecture_id)

    if lecture.status.value != "Created":
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Analyze already started")

    file_suffix = Path(lecture.filename).suffix

    if lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found")

    try:
        await minio.client.stat_object(
            bucket_name=SETTINGS.s3_bucket, object_name=str(lecture_id) + file_suffix
        )
    except S3Error:
        raise HTTPException(status_code=404, detail="Lecture file not found")

    await set_lecture_status(edgedb.client, id=lecture_id, status="Processing")
    await arq.client.enqueue_job("analyze", lecture_id=lecture_id, _job_id=str(lecture_id))


@router.get("/{lecture_id}/status")
async def get_status(lecture_id: UUID) -> LectureStatus:
    lecture = await get_lecture(edgedb.client, id=lecture_id)

    return LectureStatus(status=lecture.status.value)
