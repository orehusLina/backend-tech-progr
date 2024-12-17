from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.vacancy_skill import VacancySkillSchema
from project.infrastructure.postgres.repository.vacancy_skill_repo import VacancySkillRepository

router = APIRouter()
repository = VacancySkillRepository()


@router.post("/vacancies/{vacancy_id}/skills/", response_model=VacancySkillSchema)
async def add_skill_to_vacancy(vacancy_id: int, skill_data: VacancySkillSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.add_skill_to_vacancy(session, vacancy_id, skill_data.skill_id)


@router.get("/vacancies/{vacancy_id}/skills/", response_model=list[VacancySkillSchema])
async def get_skills_for_vacancy(vacancy_id: int, session: AsyncSession = Depends(get_async_session)):
    return await repository.get_skills_for_vacancy(session, vacancy_id)


@router.delete("/vacancies/{vacancy_id}/skills/{skill_id}")
async def delete_skill_from_vacancy(vacancy_id: int, skill_id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_skill_from_vacancy(session, vacancy_id, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill for vacancy not found")
    return {"detail": "Skill deleted successfully"}
