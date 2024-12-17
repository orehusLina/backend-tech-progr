from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.vacancy_skill import VacancySkillSchema
from project.infrastructure.postgres.models import VacancySkill
from project.core.config import settings


class VacancySkillRepository:
    _collection: Type[VacancySkill] = VacancySkill

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def add_skill_to_vacancy(self, session: AsyncSession, vacancy_id: int, skill_id: int) -> VacancySkillSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.vacancy_skills (vacancy_id, skill_id)
        VALUES (:vacancy_id, :skill_id)
        RETURNING *;
        """
        result = await session.execute(text(query), {"vacancy_id": vacancy_id, "skill_id": skill_id})
        row = result.mappings().first()
        await session.commit()
        return VacancySkillSchema.model_validate(obj=row)

    async def get_skills_for_vacancy(self, session: AsyncSession, vacancy_id: int) -> list[VacancySkillSchema]:
        query = f"""
        SELECT * FROM {settings.POSTGRES_SCHEMA}.vacancy_skills 
        WHERE vacancy_id = :vacancy_id;
        """
        result = await session.execute(text(query), {"vacancy_id": vacancy_id})
        return [VacancySkillSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def delete_skill_from_vacancy(self, session: AsyncSession, vacancy_id: int, skill_id: int) -> bool:
        query = f"""
        DELETE FROM {settings.POSTGRES_SCHEMA}.vacancy_skills 
        WHERE vacancy_id = :vacancy_id AND skill_id = :skill_id;
        """
        result = await session.execute(text(query), {"vacancy_id": vacancy_id, "skill_id": skill_id})
        await session.commit()
        return result.rowcount > 0
