from uuid import UUID

from pydantic import BaseModel


class PreviewLecture(BaseModel):
    id: UUID
    status: str
    filename: str
    text: str | None
    error: str | None
