from sqlalchemy import Date, CHAR
from sqlalchemy.orm import Mapped, mapped_column
from project.infrastructure.postgres.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_name: Mapped[str] = mapped_column(CHAR(50), nullable=False)
    phone: Mapped[str] = mapped_column(CHAR(20), nullable=True)
    email: Mapped[str] = mapped_column(CHAR(50), nullable=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)
