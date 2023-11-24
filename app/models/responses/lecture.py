from uuid import UUID

from pydantic import BaseModel


class Lecture(BaseModel):
    id: UUID
    status: str
    filename: str
    object_name: str | None
    text: str | None
