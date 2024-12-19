from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.resume_vacancy import ResumeVacancySchema
from project.infrastructure.postgres.repository.resume_vacancy_repo import ResumeVacancyRepository

router = APIRouter()
repo = ResumeVacancyRepository()


@router.post("/", response_model=ResumeVacancySchema)
async def create_resume_vacancy(data: ResumeVacancySchema, session: AsyncSession = Depends(get_async_session)):
    return await repo.create(session, data.model_dump())


@router.get("/", response_model=list[ResumeVacancySchema])
async def get_all_resume_vacancies(session: AsyncSession = Depends(get_async_session)):
    return await repo.get_all(session)


@router.get("/{resume_id}/{vacancy_id}", response_model=ResumeVacancySchema)
async def get_resume_vacancy(resume_id: int, vacancy_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await repo.get(session, resume_id, vacancy_id)
    if not result:
        raise HTTPException(status_code=404, detail="Resume vacancy not found")
    return result


@router.put("/{resume_id}/{vacancy_id}", response_model=ResumeVacancySchema)
async def update_resume_vacancy(
    resume_id: int, vacancy_id: int, data: dict, session: AsyncSession = Depends(get_async_session)
):
    result = await repo.update(session, resume_id, vacancy_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Resume vacancy not found")
    return result


@router.delete("/{resume_id}/{vacancy_id}", response_model=dict)
async def delete_resume_vacancy(resume_id: int, vacancy_id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repo.delete(session, resume_id, vacancy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resume vacancy not found")
    return {"detail": "Resume vacancy deleted successfully"}
