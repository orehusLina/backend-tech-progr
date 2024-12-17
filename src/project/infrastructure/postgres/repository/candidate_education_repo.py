from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.candidate_education import CandidateEducationSchema
from project.infrastructure.postgres.models import CandidateEducation
from project.core.config import settings


class CandidateEducationRepository:
    _collection: Type[CandidateEducation] = CandidateEducation

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def add_education_to_candidate(self, session: AsyncSession, education_data: dict) -> CandidateEducationSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.candidates_education 
        (candidate_id, education_id, graduation_year, degree, field_of_study)
        VALUES (:candidate_id, :education_id, :graduation_year, :degree, :field_of_study)
        RETURNING *;
        """
        result = await session.execute(text(query), education_data)
        row = result.mappings().first()
        await session.commit()
        return CandidateEducationSchema.model_validate(obj=row)

    async def get_education_for_candidate(self, session: AsyncSession, candidate_id: int) -> list[CandidateEducationSchema]:
        query = f"""
        SELECT * FROM {settings.POSTGRES_SCHEMA}.candidates_education 
        WHERE candidate_id = :candidate_id;
        """
        result = await session.execute(text(query), {"candidate_id": candidate_id})
        return [CandidateEducationSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def delete_education_from_candidate(self, session: AsyncSession, candidate_id: int, education_id: int) -> bool:
        query = f"""
        DELETE FROM {settings.POSTGRES_SCHEMA}.candidates_education 
        WHERE candidate_id = :candidate_id AND education_id = :education_id;
        """
        result = await session.execute(text(query), {"candidate_id": candidate_id, "education_id": education_id})
        await session.commit()
        return result.rowcount > 0
