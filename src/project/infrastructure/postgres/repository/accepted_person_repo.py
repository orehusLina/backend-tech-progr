from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.accepted_person import AcceptedPersonSchema
from project.core.config import settings
from typing import List


class AcceptedPersonRepository:
    async def add_accepted_person(self, session: AsyncSession, data: dict) -> AcceptedPersonSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.accepted_person 
        (candidate_id, vacancy_id, date_of_acceptance)
        VALUES (:candidate_id, :vacancy_id, :date_of_acceptance)
        RETURNING *;
        """
        result = await session.execute(text(query), data)
        row = result.mappings().first()
        await session.commit()
        return AcceptedPersonSchema.model_validate(obj=row)

    async def get_all_accepted(self, session: AsyncSession) -> List[AcceptedPersonSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.accepted_person;"
        result = await session.execute(text(query))
        return [AcceptedPersonSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_accepted_by_vacancy(self, session: AsyncSession, vacancy_id: int) -> AcceptedPersonSchema | None:
        query = f"""
        SELECT * FROM {settings.POSTGRES_SCHEMA}.accepted_person 
        WHERE vacancy_id = :vacancy_id;
        """
        result = await session.execute(text(query), {"vacancy_id": vacancy_id})
        row = result.mappings().first()
        return AcceptedPersonSchema.model_validate(obj=row) if row else None

    async def delete_accepted_person(self, session: AsyncSession, candidate_id: int, vacancy_id: int) -> bool:
        query = f"""
        DELETE FROM {settings.POSTGRES_SCHEMA}.accepted_person
        WHERE candidate_id = :candidate_id AND vacancy_id = :vacancy_id;
        """
        result = await session.execute(text(query), {"candidate_id": candidate_id, "vacancy_id": vacancy_id})
        await session.commit()
        return result.rowcount > 0
