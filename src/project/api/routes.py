from fastapi import APIRouter

from project.infrastructure.postgres.repository.candidate_repo import CandidateRepository
from project.infrastructure.postgres.database import PostgresDatabase
from project.schemas.candidate import CandidateSchema

router = APIRouter()


@router.get("/all_candidates", response_model=list[CandidateSchema])
async def get_all_candidates() -> list[CandidateSchema]:
    candidate_repo = CandidateRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await candidate_repo.check_connection(session=session)
        all_candidates = await candidate_repo.get_all_candidates(session=session)

    return all_candidates
