# AUTOGENERATED FROM:
#     'dbschema/queries/create_lecture.edgeql'
#     'dbschema/queries/delete_lectures.edgeql'
#     'dbschema/queries/finish_analysis.edgeql'
#     'dbschema/queries/get_lecture.edgeql'
#     'dbschema/queries/get_lectures.edgeql'
#     'dbschema/queries/set_lecture_status.edgeql'
# WITH:
#     $ edgedb-py --file app/queries.py


from __future__ import annotations
import dataclasses
import edgedb
import enum
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_validators__(cls):
        from pydantic.dataclasses import dataclass as pydantic_dataclass

        pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class CreateLectureResult(NoPydanticValidation):
    id: uuid.UUID
    object_name: str | None


@dataclasses.dataclass
class DeleteLecturesResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class GetLectureResult(NoPydanticValidation):
    id: uuid.UUID
    status: LectureStatus
    filename: str | None
    object_name: str | None
    text: str | None


class LectureStatus(enum.Enum):
    CREATED = "Created"
    PROCESSING = "Processing"
    PROCESSED = "Processed"
    ERROR = "Error"


async def create_lecture(
    executor: edgedb.AsyncIOExecutor,
    *,
    filename: str,
) -> CreateLectureResult:
    return await executor.query_single(
        """\
        with result := (insert Lecture {
            file := (insert File {
                filename := <str>$filename
            })
        })

        select result { id, object_name := <str>(.file.id) }\
        """,
        filename=filename,
    )


async def delete_lectures(
    executor: edgedb.AsyncIOExecutor,
) -> list[DeleteLecturesResult]:
    return await executor.query(
        """\
        delete Lecture;\
        """,
    )


async def finish_analysis(
    executor: edgedb.AsyncIOExecutor,
    *,
    lecture_id: uuid.UUID,
    status: str | None,
    text: str | None,
    error: str | None,
) -> DeleteLecturesResult | None:
    return await executor.query_single(
        """\
        update Lecture
        filter .id = <uuid>$lecture_id
        set {
            status := <optional str>$status,
            text := <optional str>$text,
            error := <optional str>$error
        }\
        """,
        lecture_id=lecture_id,
        status=status,
        text=text,
        error=error,
    )


async def get_lecture(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
) -> GetLectureResult | None:
    return await executor.query_single(
        """\
        select Lecture {
            id,
            status,
            filename := .file.filename,
            object_name := <str>(.file.id),
            text := .text
        }
        filter .id = <uuid>$id
        limit 1\
        """,
        id=id,
    )


async def get_lectures(
    executor: edgedb.AsyncIOExecutor,
) -> list[GetLectureResult]:
    return await executor.query(
        """\
        select Lecture {
            id,
            status,
            filename := .file.filename,
            object_name := <str>(.file.id),
            text := .text
        }\
        """,
    )


async def set_lecture_status(
    executor: edgedb.AsyncIOExecutor,
    *,
    id: uuid.UUID,
    status: str,
) -> DeleteLecturesResult | None:
    return await executor.query_single(
        """\
        update Lecture
        filter .id = <uuid>$id
        set {
            status := <str>$status
        }\
        """,
        id=id,
        status=status,
    )
