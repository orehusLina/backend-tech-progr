from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.skill import SkillSchema
from project.infrastructure.postgres.repository.skill_repo import SkillRepository

router = APIRouter()
repository = SkillRepository()


@router.post("/skills/", response_model=SkillSchema)
async def create_skill(skill: SkillSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.create_skill(session, skill.model_dump())


@router.get("/skills/", response_model=list[SkillSchema])
async def get_all_skills(session: AsyncSession = Depends(get_async_session)):
    return await repository.get_all_skills(session)


@router.get("/skills/{id}", response_model=SkillSchema)
async def get_skill_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    skill = await repository.get_skill_by_id(session, id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.delete("/skills/{id}")
async def delete_skill(id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_skill(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"detail": "Skill deleted successfully"}
