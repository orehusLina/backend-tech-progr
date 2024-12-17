from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class ResumeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resume_id: int
    candidate_id: int
    job_title: str = Field(max_length=50)
    work_experience: int
    content: str
    date_created: date
