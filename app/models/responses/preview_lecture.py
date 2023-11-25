from uuid import UUID

from pydantic import BaseModel


class PreviewLecture(BaseModel):
    id: UUID
    status: str
    filename: str
    error: str | None
