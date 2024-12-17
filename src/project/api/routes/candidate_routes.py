from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.candidate import CandidateSchema
from project.infrastructure.postgres.repository.candidate_repo import CandidateRepository

router = APIRouter()
repository = CandidateRepository()


@router.post("/candidates/", response_model=CandidateSchema)
async def create_candidate(candidate: CandidateSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.create_candidate(session, candidate.model_dump())


@router.get("/candidates/", response_model=list[CandidateSchema])
async def get_all_candidates(session: AsyncSession = Depends(get_async_session)):
    return await repository.get_all_candidates(session)


@router.get("/candidates/{id}", response_model=CandidateSchema)
async def get_candidate_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    candidate = await repository.get_candidate_by_id(session, id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.put("/candidates/{id}", response_model=CandidateSchema)
async def update_candidate(id: int, candidate: CandidateSchema, session: AsyncSession = Depends(get_async_session)):
    updated_candidate = await repository.update_candidate(session, id, candidate.model_dump())
    if not updated_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return updated_candidate


@router.delete("/candidates/{id}")
async def delete_candidate(id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_candidate(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"detail": "Candidate deleted successfully"}
