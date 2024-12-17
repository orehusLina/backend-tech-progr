from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.accepted_person import AcceptedPersonSchema
from project.infrastructure.postgres.repository.accepted_person_repo import AcceptedPersonRepository

router = APIRouter()
repository = AcceptedPersonRepository()


@router.post("/accepted_person/", response_model=AcceptedPersonSchema)
async def add_accepted_person(accepted_person: AcceptedPersonSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.add_accepted_person(session, accepted_person.model_dump())


@router.get("/accepted_person/", response_model=list[AcceptedPersonSchema])
async def get_all_accepted(session: AsyncSession = Depends(get_async_session)):
    return await repository.get_all_accepted(session)


@router.get("/accepted_person/by_vacancy/{vacancy_id}", response_model=AcceptedPersonSchema)
async def get_accepted_by_vacancy(vacancy_id: int, session: AsyncSession = Depends(get_async_session)):
    accepted = await repository.get_accepted_by_vacancy(session, vacancy_id)
    if not accepted:
        raise HTTPException(status_code=404, detail="No accepted candidate for this vacancy")
    return accepted


@router.delete("/accepted_person/{candidate_id}/{vacancy_id}")
async def delete_accepted_person(candidate_id: int, vacancy_id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_accepted_person(session, candidate_id, vacancy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Accepted person not found")
    return {"detail": "Accepted person record deleted successfully"}
