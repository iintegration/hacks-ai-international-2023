from pydantic import BaseModel


class CreateLecture(BaseModel):
    filename: str
