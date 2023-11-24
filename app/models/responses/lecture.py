from uuid import UUID

from pydantic import BaseModel


class Lecture(BaseModel):
    id: UUID
    status: str
    filename: str
    text: str | None
    error: str | None
    download_link: str | None
