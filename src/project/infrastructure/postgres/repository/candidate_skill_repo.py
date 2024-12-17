from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.candidate_skill import CandidateSkillSchema
from project.infrastructure.postgres.models import CandidateSkill
from project.core.config import settings


class CandidateSkillRepository:
    _collection: Type[CandidateSkill] = CandidateSkill

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def add_skill_to_candidate(self, session: AsyncSession, candidate_id: int, skill_id: int) -> CandidateSkillSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.candidates_skills (candidate_id, skill_id)
        VALUES (:candidate_id, :skill_id)
        RETURNING *;
        """
        result = await session.execute(text(query), {"candidate_id": candidate_id, "skill_id": skill_id})
        row = result.mappings().first()
        await session.commit()
        return CandidateSkillSchema.model_validate(obj=row)

    async def get_skills_for_candidate(self, session: AsyncSession, candidate_id: int) -> list[CandidateSkillSchema]:
        query = f"""
        SELECT * FROM {settings.POSTGRES_SCHEMA}.candidates_skills 
        WHERE candidate_id = :candidate_id;
        """
        result = await session.execute(text(query), {"candidate_id": candidate_id})
        return [CandidateSkillSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def delete_skill_from_candidate(self, session: AsyncSession, candidate_id: int, skill_id: int) -> bool:
        query = f"""
        DELETE FROM {settings.POSTGRES_SCHEMA}.candidates_skills 
        WHERE candidate_id = :candidate_id AND skill_id = :skill_id;
        """
        result = await session.execute(text(query), {"candidate_id": candidate_id, "skill_id": skill_id})
        await session.commit()
        return result.rowcount > 0
