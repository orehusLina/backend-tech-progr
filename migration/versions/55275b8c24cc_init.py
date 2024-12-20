"""init

Revision ID: 55275b8c24cc
Revises: 
Create Date: 2024-12-16 00:28:37.414497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision: str = '55275b8c24cc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('candidates',
    sa.Column('candidate_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('candidate_name', sa.CHAR(length=50), nullable=False),
    sa.Column('phone', sa.CHAR(length=20), nullable=True),
    sa.Column('email', sa.CHAR(length=50), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('candidate_id'),
    schema=settings.POSTGRES_SCHEMA
    )


def downgrade() -> None:
    op.drop_table('candidates', schema=settings.POSTGRES_SCHEMA)
