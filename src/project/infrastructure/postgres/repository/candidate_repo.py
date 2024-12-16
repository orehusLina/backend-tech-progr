from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from project.schemas.candidate import CandidateSchema
from project.infrastructure.postgres.models import Candidate

from project.core.config import settings


class CandidateRepository:
    _collection: Type[Candidate] = Candidate

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_candidates(
        self,
        session: AsyncSession,
    ) -> list[CandidateSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.candidate;"

        users = await session.execute(text(query))

        return [CandidateSchema.model_validate(obj=candidate) for candidate in candidates.mappings().all()]

