from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.resume_vacancy import ResumeVacancySchema
from project.core.config import settings
from typing import List


class ResumeVacancyRepository:
    async def create(self, session: AsyncSession, data: dict) -> ResumeVacancySchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.resume_vacancies 
        (resume_id, vacancy_id, date_applied, status_approved)
        VALUES (:resume_id, :vacancy_id, :date_applied, :status_approved)
        RETURNING *;
        """
        result = await session.execute(text(query), data)
        row = result.mappings().first()
        await session.commit()
        return ResumeVacancySchema.model_validate(obj=row)

    async def get_all(self, session: AsyncSession) -> List[ResumeVacancySchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.resume_vacancies;"
        result = await session.execute(text(query))
        return [ResumeVacancySchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get(self, session: AsyncSession, resume_id: int, vacancy_id: int) -> ResumeVacancySchema | None:
        query = f"""
        SELECT * FROM {settings.POSTGRES_SCHEMA}.resume_vacancies
        WHERE resume_id = :resume_id AND vacancy_id = :vacancy_id;
        """
        result = await session.execute(text(query), {"resume_id": resume_id, "vacancy_id": vacancy_id})
        row = result.mappings().first()
        return ResumeVacancySchema.model_validate(obj=row) if row else None

    async def update(self, session: AsyncSession, resume_id: int, vacancy_id: int, update_data: dict) -> ResumeVacancySchema | None:
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.resume_vacancies
        SET date_applied = COALESCE(:date_applied, date_applied),
            status_approved = COALESCE(:status_approved, status_approved)
        WHERE resume_id = :resume_id AND vacancy_id = :vacancy_id
        RETURNING *;
        """
        update_data.update({"resume_id": resume_id, "vacancy_id": vacancy_id})
        result = await session.execute(text(query), update_data)
        row = result.mappings().first()
        await session.commit()
        return ResumeVacancySchema.model_validate(obj=row) if row else None

    async def delete(self, session: AsyncSession, resume_id: int, vacancy_id: int) -> bool:
        query = f"""
        DELETE FROM {settings.POSTGRES_SCHEMA}.resume_vacancies
        WHERE resume_id = :resume_id AND vacancy_id = :vacancy_id;
        """
        result = await session.execute(text(query), {"resume_id": resume_id, "vacancy_id": vacancy_id})
        await session.commit()
        return result.rowcount > 0
