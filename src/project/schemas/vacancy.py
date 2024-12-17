from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class VacancySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vacancy_id: int
    employer_id: int
    job_title: str = Field(max_length=50)
    salary: float
    work_experience: int
    status_open: bool | None = Field(default=None)
    job_description: str | None = Field(default=None)
    date_posted: date | None = Field(default=None)
