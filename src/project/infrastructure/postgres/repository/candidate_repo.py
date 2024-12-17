from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.candidate import CandidateSchema
from project.infrastructure.postgres.models import Candidate
from project.core.config import settings


class CandidateRepository:
    _collection: Type[Candidate] = Candidate

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_candidate(self, session: AsyncSession, candidate_data: dict) -> CandidateSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.candidates 
        (name, email, phone, resume, experience, applied_vacancy_id)
        VALUES (:name, :email, :phone, :resume, :experience, :applied_vacancy_id)
        RETURNING *;
        """
        result = await session.execute(text(query), candidate_data)
        row = result.mappings().first()
        await session.commit()
        return CandidateSchema.model_validate(obj=row)

    async def get_all_candidates(self, session: AsyncSession) -> list[CandidateSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.candidates;"
        result = await session.execute(text(query))
        return [CandidateSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_candidate_by_id(self, session: AsyncSession, candidate_id: int) -> CandidateSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.candidates WHERE candidate_id = :candidate_id;"
        result = await session.execute(text(query), {"candidate_id": candidate_id})
        row = result.mappings().first()
        return CandidateSchema.model_validate(obj=row) if row else None

    async def update_candidate(self, session: AsyncSession, candidate_id: int, update_data: dict) -> CandidateSchema | None:
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.candidates
        SET name = :name, email = :email, phone = :phone, resume = :resume, 
            experience = :experience, applied_vacancy_id = :applied_vacancy_id
        WHERE candidate_id = :candidate_id
        RETURNING *;
        """
        update_data["candidate_id"] = candidate_id
        result = await session.execute(text(query), update_data)
        row = result.mappings().first()
        await session.commit()
        return CandidateSchema.model_validate(obj=row) if row else None

    async def delete_candidate(self, session: AsyncSession, candidate_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.candidates WHERE candidate_id = :candidate_id;"
        result = await session.execute(text(query), {"candidate_id": candidate_id})
        await session.commit()
        return result.rowcount > 0
