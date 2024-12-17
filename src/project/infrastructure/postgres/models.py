from sqlalchemy import ForeignKey, DECIMAL, Boolean, Date, Text, CHAR
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from project.infrastructure.postgres.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_name: Mapped[str] = mapped_column(CHAR(50), nullable=False)
    phone: Mapped[str] = mapped_column(CHAR(20), nullable=True)
    email: Mapped[str] = mapped_column(CHAR(50), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)


class Resume(Base):
    __tablename__ = "resumes"
    resume_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id"), nullable=False)
    job_title: Mapped[str] = mapped_column(CHAR(50), nullable=False)
    work_experience: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_created: Mapped[date] = mapped_column(Date, nullable=False)
    candidate: Mapped["Candidate"] = relationship(back_populates="resumes")


class Employer(Base):
    __tablename__ = "employers"
    employer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employer_name: Mapped[str] = mapped_column(CHAR(50), nullable=False)
    contact_name: Mapped[str] = mapped_column(CHAR(50), nullable=True)
    phone: Mapped[str] = mapped_column(CHAR(20), nullable=True)
    email: Mapped[str] = mapped_column(CHAR(50), nullable=True)
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="employer")


class Vacancy(Base):
    __tablename__ = "vacancies"
    vacancy_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.employer_id"), nullable=False)
    job_title: Mapped[str] = mapped_column(CHAR(50), nullable=False)
    salary: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    work_experience: Mapped[int] = mapped_column(nullable=False)
    status_open: Mapped[bool] = mapped_column(Boolean, nullable=True)
    job_description: Mapped[str] = mapped_column(Text, nullable=True)
    date_posted: Mapped[date] = mapped_column(Date, nullable=True)
    employer: Mapped["Employer"] = relationship(back_populates="vacancies")
    skills: Mapped[list["VacancySkill"]] = relationship(back_populates="vacancy")


class Skill(Base):
    __tablename__ = "skills"
    skill_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    skill_name: Mapped[str] = mapped_column(CHAR(50), nullable=False)


class VacancySkill(Base):
    __tablename__ = "vacancy_skills"
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.vacancy_id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.skill_id"), primary_key=True)
    vacancy: Mapped["Vacancy"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship()


class EducationOrganization(Base):
    __tablename__ = "education_organization"
    education_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization_name: Mapped[str] = mapped_column(CHAR(50), nullable=True)


class CandidateEducation(Base):
    __tablename__ = "candidates_education"
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id"), primary_key=True)
    education_id: Mapped[int] = mapped_column(ForeignKey("education_organization.education_id"), primary_key=True)
    graduation_year: Mapped[int] = mapped_column(nullable=True)
    degree: Mapped[str] = mapped_column(CHAR(50), nullable=True)
    field_of_study: Mapped[str] = mapped_column(CHAR(50), nullable=True)


class CandidateSkill(Base):
    __tablename__ = "candidates_skills"
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.skill_id"), primary_key=True)


class ResumeVacancy(Base):
    __tablename__ = "resume_vacancies"
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.resume_id"), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.vacancy_id"), primary_key=True)
    date_applied: Mapped[date] = mapped_column(Date, nullable=False)
    status_approved: Mapped[bool] = mapped_column(Boolean, nullable=True)


class AcceptedPerson(Base):
    __tablename__ = "accepted_person"
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.candidate_id"), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.vacancy_id"), primary_key=True)
    date_of_acceptance: Mapped[date] = mapped_column(Date, nullable=True)
