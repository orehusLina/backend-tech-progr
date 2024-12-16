from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class CandidateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    candidate_id: int
    candidate_name: str
    phone: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=50)
    birth_date: date | None = Field(default=None)
