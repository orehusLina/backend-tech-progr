from .employer_routes import router as employer_router
from .vacancy_routes import router as vacancy_router
from .candidate_routes import router as candidate_router
from .resume_routes import router as resume_router
from .skill_routes import router as skill_router
from .candidate_skill_routes import router as candidate_skill_router
from .vacancy_skill_routes import router as vacancy_skill_router
from .education_organization_routes import router as education_router
from .candidate_education_routes import router as candidate_education_router
from .accepted_person_routes import router as accepted_person_router
from .resume_vacancy_routes import router as resume_vacancy_router

from fastapi import APIRouter

router = APIRouter()
router.include_router(employer_router, prefix="/employers", tags=["Employers"])
router.include_router(vacancy_router, prefix="/vacancies", tags=["Vacancies"])
router.include_router(candidate_router, prefix="/candidates", tags=["Candidates"])
router.include_router(resume_router, prefix="/resumes", tags=["Resumes"])
router.include_router(skill_router, prefix="/skills", tags=["Skills"])
router.include_router(candidate_skill_router, prefix="/candidates", tags=["Candidates_Skills"])
router.include_router(vacancy_skill_router, prefix="/vacancies", tags=["Vacancy_Skills"])
router.include_router(education_router, prefix="/education", tags=["Education"])
router.include_router(candidate_education_router, prefix="/candidates", tags=["Candidates_Education"])
router.include_router(accepted_person_router, prefix="/accepted_person", tags=["Accepted_Person"])
router.include_router(resume_vacancy_router, prefix="/resume_vacancies", tags=["Resume_Vacancies"])
