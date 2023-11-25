from uuid import UUID

from pydantic import BaseModel

from app.models.responses.term import Term


class Lecture(BaseModel):
    id: UUID
    status: str
    filename: str
    text: str | None
    timestamps: list[dict] | None
    error: str | None
    download_link: str | None
    terms: list[Term]
