from uuid import UUID

from pydantic import BaseModel


class CreatedLecture(BaseModel):
    id: UUID
    upload_url: str
