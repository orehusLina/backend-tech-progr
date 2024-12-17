from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class AcceptedPersonSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    candidate_id: int
    vacancy_id: int
    date_of_acceptance: date | None = Field(default=None)
