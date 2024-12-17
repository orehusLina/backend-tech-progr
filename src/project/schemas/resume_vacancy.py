from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class ResumeVacancySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resume_id: int
    vacancy_id: int
    date_applied: date
    status_approved: bool | None = Field(default=None)
