from pydantic import BaseModel, Field, ConfigDict


class EducationOrganizationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    education_id: int
    organization_name: str = Field(max_length=50)
