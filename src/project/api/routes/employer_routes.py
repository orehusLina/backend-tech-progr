from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.employer import EmployerSchema
from project.infrastructure.postgres.repository.employer_repo import EmployerRepository

router = APIRouter()
repository = EmployerRepository()


@router.post("/employers/", response_model=EmployerSchema)
async def create_employer(employer: EmployerSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.create_employer(session, employer.model_dump())


@router.get("/employers/", response_model=list[EmployerSchema])
async def get_all_employers(session: AsyncSession = Depends(get_async_session)):
    return await repository.get_all_employers(session)


@router.get("/employers/{id}", response_model=EmployerSchema)
async def get_employer_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    employer = await repository.get_employer_by_id(session, id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer


@router.put("/employers/{id}", response_model=EmployerSchema)
async def update_employer(id: int, employer: EmployerSchema, session: AsyncSession = Depends(get_async_session)):
    updated_employer = await repository.update_employer(session, id, employer.model_dump())
    if not updated_employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return updated_employer


@router.delete("/employers/{id}")
async def delete_employer(id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_employer(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Employer not found")
    return {"detail": "Employer deleted successfully"}
