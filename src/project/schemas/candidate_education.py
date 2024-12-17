from pydantic import BaseModel, Field, ConfigDict


class CandidateEducationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    candidate_id: int
    education_id: int
    graduation_year: int | None = Field(default=None)
    degree: str | None = Field(default=None, max_length=50)
    field_of_study: str | None = Field(default=None, max_length=50)
