from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.candidate_skill import CandidateSkillSchema
from project.infrastructure.postgres.repository.candidate_skill_repo import CandidateSkillRepository

router = APIRouter()
repository = CandidateSkillRepository()


@router.post("/candidates/{candidate_id}/skills/", response_model=CandidateSkillSchema)
async def add_skill_to_candidate(candidate_id: int, skill_data: CandidateSkillSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.add_skill_to_candidate(session, candidate_id, skill_data.skill_id)


@router.get("/candidates/{candidate_id}/skills/", response_model=list[CandidateSkillSchema])
async def get_skills_for_candidate(candidate_id: int, session: AsyncSession = Depends(get_async_session)):
    return await repository.get_skills_for_candidate(session, candidate_id)


@router.delete("/candidates/{candidate_id}/skills/{skill_id}")
async def delete_skill_from_candidate(candidate_id: int, skill_id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_skill_from_candidate(session, candidate_id, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill for candidate not found")
    return {"detail": "Skill deleted successfully"}
