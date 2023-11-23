from pydantic import BaseModel


class LectureStatus(BaseModel):
    status: str
