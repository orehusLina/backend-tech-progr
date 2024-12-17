from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.resume import ResumeSchema
from project.infrastructure.postgres.repository.resume_repo import ResumeRepository

router = APIRouter()
repository = ResumeRepository()


@router.post("/resumes/", response_model=ResumeSchema)
async def create_resume(resume: ResumeSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.create_resume(session, resume.model_dump())


@router.get("/resumes/", response_model=list[ResumeSchema])
async def get_all_resumes(session: AsyncSession = Depends(get_async_session)):
    return await repository.get_all_resumes(session)


@router.get("/resumes/{id}", response_model=ResumeSchema)
async def get_resume_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    resume = await repository.get_resume_by_id(session, id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.put("/resumes/{id}", response_model=ResumeSchema)
async def update_resume(id: int, resume: ResumeSchema, session: AsyncSession = Depends(get_async_session)):
    updated_resume = await repository.update_resume(session, id, resume.model_dump())
    if not updated_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return updated_resume


@router.delete("/resumes/{id}")
async def delete_resume(id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_resume(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"detail": "Resume deleted successfully"}


@router.get("/resumes/by_candidate/{candidate_id}", response_model=list[ResumeSchema])
async def get_resumes_by_candidate(candidate_id: int, session: AsyncSession = Depends(get_async_session)):
    return await repository.get_resumes_by_candidate(session, candidate_id)


@router.get("/resumes/by_vacancy/{vacancy_id}", response_model=list[ResumeSchema])
async def get_resumes_by_vacancy(vacancy_id: int, session: AsyncSession = Depends(get_async_session)):
    return await repository.get_resumes_by_vacancy(session, vacancy_id)
