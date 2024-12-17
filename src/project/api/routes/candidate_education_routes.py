from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.candidate_education import CandidateEducationSchema
from project.infrastructure.postgres.repository.candidate_education_repo import CandidateEducationRepository

router = APIRouter()
repository = CandidateEducationRepository()


@router.post("/candidates/{candidate_id}/education/", response_model=CandidateEducationSchema)
async def add_education_to_candidate(candidate_id: int, education: CandidateEducationSchema, session: AsyncSession = Depends(get_async_session)):
    education_data = education.model_dump()
    education_data["candidate_id"] = candidate_id
    return await repository.add_education_to_candidate(session, education_data)


@router.get("/candidates/{candidate_id}/education/", response_model=list[CandidateEducationSchema])
async def get_education_for_candidate(candidate_id: int, session: AsyncSession = Depends(get_async_session)):
    return await repository.get_education_for_candidate(session, candidate_id)


@router.delete("/candidates/{candidate_id}/education/{education_id}")
async def delete_education_from_candidate(candidate_id: int, education_id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_education_from_candidate(session, candidate_id, education_id)
    if not success:
        raise HTTPException(status_code=404, detail="Education record not found for candidate")
    return {"detail": "Education record deleted successfully"}
