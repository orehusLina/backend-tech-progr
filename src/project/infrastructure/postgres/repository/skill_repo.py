from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from project.schemas.skill import SkillSchema
from project.infrastructure.postgres.models import Skill
from project.core.config import settings


class SkillRepository:
    _collection: Type[Skill] = Skill

    async def check_connection(self, session: AsyncSession) -> bool:
        query = "SELECT 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def create_skill(self, session: AsyncSession, skill_data: dict) -> SkillSchema:
        query = f"""
        INSERT INTO {settings.POSTGRES_SCHEMA}.skills (skill_name)
        VALUES (:skill_name)
        RETURNING *;
        """
        result = await session.execute(text(query), skill_data)
        row = result.mappings().first()
        await session.commit()
        return SkillSchema.model_validate(obj=row)

    async def get_all_skills(self, session: AsyncSession) -> list[SkillSchema]:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.skills;"
        result = await session.execute(text(query))
        return [SkillSchema.model_validate(obj=row) for row in result.mappings().all()]

    async def get_skill_by_id(self, session: AsyncSession, skill_id: int) -> SkillSchema | None:
        query = f"SELECT * FROM {settings.POSTGRES_SCHEMA}.skills WHERE skill_id = :skill_id;"
        result = await session.execute(text(query), {"skill_id": skill_id})
        row = result.mappings().first()
        return SkillSchema.model_validate(obj=row) if row else None

    async def delete_skill(self, session: AsyncSession, skill_id: int) -> bool:
        query = f"DELETE FROM {settings.POSTGRES_SCHEMA}.skills WHERE skill_id = :skill_id;"
        result = await session.execute(text(query), {"skill_id": skill_id})
        await session.commit()
        return result.rowcount > 0
