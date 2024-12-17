from pydantic import BaseModel, ConfigDict


class VacancySkillSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vacancy_id: int
    skill_id: int
