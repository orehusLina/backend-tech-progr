from pydantic import BaseModel, Field, ConfigDict


class SkillSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skill_id: int
    skill_name: str = Field(max_length=50)
