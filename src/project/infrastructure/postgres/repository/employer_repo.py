from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.employer import EmployerSchema
from project.infrastructure.postgres.models import Employer
from project.core.config import settings


class EmployerRepository:
    _collection: Type[Employer] = Employer

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_employer(self, session: AsyncSession, employer_data: dict) -> EmployerSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.employers (name, company, email)
        VALUES (:name, :company, :email)
        RETURNING *;
        """
        result = await session.execute(text(query), employer_data)
        row = result.mappings().first()
        await session.commit()
        return EmployerSchema.model_validate(obj=row)

    async def get_all_employers(self, session: AsyncSession) -> list[EmployerSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.employers;"
        result = await session.execute(text(query))
        return [EmployerSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_employer_by_id(self, session: AsyncSession, employer_id: int) -> EmployerSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.employers WHERE employer_id = :employer_id;"
        result = await session.execute(text(query), {"employer_id": employer_id})
        row = result.mappings().first()
        return EmployerSchema.model_validate(obj=row) if row else None

    async def update_employer(self, session: AsyncSession, employer_id: int, update_data: dict) -> EmployerSchema | None:
        query = f"""
        UPDATE {settings.POSTGRES_SCHEMA}.employers
        SET name = :name, company = :company, email = :email
        WHERE employer_id = :employer_id
        RETURNING *;
        """
        update_data["employer_id"] = employer_id
        result = await session.execute(text(query), update_data)
        row = result.mappings().first()
        await session.commit()
        return EmployerSchema.model_validate(obj=row) if row else None

    async def delete_employer(self, session: AsyncSession, employer_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.employers WHERE employer_id = :employer_id;"
        result = await session.execute(text(query), {"employer_id": employer_id})
        await session.commit()
        return result.rowcount > 0
