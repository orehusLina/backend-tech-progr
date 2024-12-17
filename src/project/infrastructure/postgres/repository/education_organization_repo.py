from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.education_organization import EducationOrganizationSchema
from project.infrastructure.postgres.models import EducationOrganization
from project.core.config import settings


class EducationOrganizationRepository:
    _collection: Type[EducationOrganization] = EducationOrganization

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_education(self, session: AsyncSession, education_data: dict) -> EducationOrganizationSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.education_organization (organization_name)
        VALUES (:organization_name)
        RETURNING *;
        """
        result = await session.execute(text(query), education_data)
        row = result.mappings().first()
        await session.commit()
        return EducationOrganizationSchema.model_validate(obj=row)

    async def get_all_education(self, session: AsyncSession) -> list[EducationOrganizationSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.education_organization;"
        result = await session.execute(text(query))
        return [EducationOrganizationSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_education_by_id(self, session: AsyncSession, education_id: int) -> EducationOrganizationSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.education_organization WHERE education_id = :education_id;"
        result = await session.execute(text(query), {"education_id": education_id})
        row = result.mappings().first()
        return EducationOrganizationSchema.model_validate(obj=row) if row else None

    async def delete_education(self, session: AsyncSession, education_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.education_organization WHERE education_id = :education_id;"
        result = await session.execute(text(query), {"education_id": education_id})
        await session.commit()
        return result.rowcount > 0
