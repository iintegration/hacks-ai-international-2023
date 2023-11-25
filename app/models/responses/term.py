from uuid import UUID

from pydantic import BaseModel


class Term(BaseModel):
    term: str
    definition: str
    start_timestamp: float
    end_timestamp: float
