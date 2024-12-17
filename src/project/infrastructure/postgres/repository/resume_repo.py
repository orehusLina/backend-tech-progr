from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.resume import ResumeSchema
from project.infrastructure.postgres.models import Resume
from project.core.config import settings


class ResumeRepository:
    _collection: Type[Resume] = Resume

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_resume(self, session: AsyncSession, resume_data: dict) -> ResumeSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.resumes 
        (candidate_id, job_title, work_experience, content, date_created)
        VALUES (:candidate_id, :job_title, :work_experience, :content, :date_created)
        RETURNING *;
        """
        result = await session.execute(text(query), resume_data)
        row = result.mappings().first()
        await session.commit()
        return ResumeSchema.model_validate(obj=row)

    async def get_all_resumes(self, session: AsyncSession) -> list[ResumeSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.resumes;"
        result = await session.execute(text(query))
        return [ResumeSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_resume_by_id(self, session: AsyncSession, resume_id: int) -> ResumeSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.resumes WHERE resume_id = :resume_id;"
        result = await session.execute(text(query), {"resume_id": resume_id})
        row = result.mappings().first()
        return ResumeSchema.model_validate(obj=row) if row else None

    async def update_resume(self, session: AsyncSession, resume_id: int, update_data: dict) -> ResumeSchema | None:
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.resumes
        SET job_title = :job_title, work_experience = :work_experience, 
            content = :content, date_created = :date_created
        WHERE resume_id = :resume_id
        RETURNING *;
        """
        update_data["resume_id"] = resume_id
        result = await session.execute(text(query), update_data)
        row = result.mappings().first()
        await session.commit()
        return ResumeSchema.model_validate(obj=row) if row else None

    async def delete_resume(self, session: AsyncSession, resume_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.resumes WHERE resume_id = :resume_id;"
        result = await session.execute(text(query), {"resume_id": resume_id})
        await session.commit()
        return result.rowcount > 0

    async def get_resumes_by_candidate(self, session: AsyncSession, candidate_id: int) -> list[ResumeSchema]:
        query = f"""
        SELECT * FROM {settings.POSTGRES_SCHEMA}.resumes 
        WHERE candidate_id = :candidate_id;
        """
        result = await session.execute(text(query), {"candidate_id": candidate_id})
        return [ResumeSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_resumes_by_vacancy(self, session: AsyncSession, vacancy_id: int) -> list[ResumeSchema]:
        query = f"""
        SELECT r.* FROM {settings.POSTGRES_SCHEMA}.resumes r
        JOIN {settings.POSTGRES_SCHEMA}.resume_vacancies rv ON r.resume_id = rv.resume_id
        WHERE rv.vacancy_id = :vacancy_id;
        """
        result = await session.execute(text(query), {"vacancy_id": vacancy_id})
        return [ResumeSchema.model_validate(obj=row) for row in result.mappings().all()]
