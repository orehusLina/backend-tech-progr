from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from project.infrastructure.postgres.database import get_async_session
from project.schemas.education_organization import EducationOrganizationSchema
from project.infrastructure.postgres.repository.education_organization_repo import EducationOrganizationRepository

router = APIRouter()
repository = EducationOrganizationRepository()


@router.post("/education/", response_model=EducationOrganizationSchema)
async def create_education(education: EducationOrganizationSchema, session: AsyncSession = Depends(get_async_session)):
    return await repository.create_education(session, education.model_dump())


@router.get("/education/", response_model=list[EducationOrganizationSchema])
async def get_all_education(session: AsyncSession = Depends(get_async_session)):
    return await repository.get_all_education(session)


@router.get("/education/{id}", response_model=EducationOrganizationSchema)
async def get_education_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    education = await repository.get_education_by_id(session, id)
    if not education:
        raise HTTPException(status_code=404, detail="Education organization not found")
    return education


@router.delete("/education/{id}")
async def delete_education(id: int, session: AsyncSession = Depends(get_async_session)):
    success = await repository.delete_education(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Education organization not found")
    return {"detail": "Education organization deleted successfully"}
