from pydantic import BaseModel, ConfigDict


class CandidateSkillSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    candidate_id: int
    skill_id: int
