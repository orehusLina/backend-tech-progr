from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.vacancy import VacancySchema
from project.infrastructure.postgres.models import Vacancy
from project.core.config import settings


class VacancyRepository:
    _collection: Type[Vacancy] = Vacancy

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_vacancy(self, session: AsyncSession, vacancy_data: dict) -> VacancySchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.vacancies 
        (employer_id, job_title, salary, work_experience, status_open, job_description, date_posted)
        VALUES (:employer_id, :job_title, :salary, :work_experience, :status_open, :job_description, :date_posted)
        RETURNING *;
        """
        result = await session.execute(text(query), vacancy_data)
        row = result.mappings().first()
        await session.commit()
        return VacancySchema.model_validate(obj=row)

    async def get_all_vacancies(self, session: AsyncSession) -> list[VacancySchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.vacancies;"
        result = await session.execute(text(query))
        return [VacancySchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_vacancy_by_id(self, session: AsyncSession, vacancy_id: int) -> VacancySchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.vacancies WHERE vacancy_id = :vacancy_id;"
        result = await session.execute(text(query), {"vacancy_id": vacancy_id})
        row = result.mappings().first()
        return VacancySchema.model_validate(obj=row) if row else None

    async def update_vacancy(self, session: AsyncSession, vacancy_id: int, update_data: dict) -> VacancySchema | None:
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.vacancies
        SET job_title = :job_title, salary = :salary, work_experience = :work_experience, 
            status_open = :status_open, job_description = :job_description, date_posted = :date_posted
        WHERE vacancy_id = :vacancy_id
        RETURNING *;
        """
        update_data["vacancy_id"] = vacancy_id
        result = await session.execute(text(query), update_data)
        row = result.mappings().first()
        await session.commit()
        return VacancySchema.model_validate(obj=row) if row else None

    async def delete_vacancy(self, session: AsyncSession, vacancy_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.vacancies WHERE vacancy_id = :vacancy_id;"
        result = await session.execute(text(query), {"vacancy_id": vacancy_id})
        await session.commit()
        return result.rowcount > 0
