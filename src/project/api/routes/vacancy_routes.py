from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.vacancy import VacancySchema
from project.infrastructure.postgres.repository.vacancy_repo import VacancyRepository

router = APIRouter()
repository = VacancyRepository()


@router.post("/vacancies/", response_model=VacancySchema)
async def create_vacancy(vacancy: VacancySchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.create_vacancy(session, vacancy.model_dump())


@router.get("/vacancies/", response_model=list[VacancySchema])
async def get_all_vacancies(session: AsyncSession = Depends(get_async_session)):
    return await repository.get_all_vacancies(session)


@router.get("/vacancies/{id}", response_model=VacancySchema)
async def get_vacancy_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    vacancy = await repository.get_vacancy_by_id(session, id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy


@router.put("/vacancies/{id}", response_model=VacancySchema)
async def update_vacancy(id: int, vacancy: VacancySchema, session: AsyncSession = Depends(get_async_session)):
    updated_vacancy = await repository.update_vacancy(session, id, vacancy.model_dump())
    if not updated_vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return updated_vacancy


@router.delete("/vacancies/{id}")
async def delete_vacancy(id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_vacancy(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return {"detail": "Vacancy deleted successfully"}
