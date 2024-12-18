"""Update columns to VARCHAR

Revision ID: a5b59ce93779
Revises: 7d508eb85503
Create Date: 2024-12-19 02:26:10.458157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5b59ce93779'
down_revision: Union[str, None] = '7d508eb85503'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('candidates', 'candidate_name',
               existing_type=sa.CHAR(length=50),
               type_=sa.String(length=50),
               existing_nullable=False,
               schema='my_app_schema')
    op.alter_column('candidates', 'phone',
               existing_type=sa.CHAR(length=20),
               type_=sa.String(length=20),
               existing_nullable=True,
               schema='my_app_schema')
    op.alter_column('candidates', 'email',
               existing_type=sa.CHAR(length=50),
               type_=sa.String(length=50),
               existing_nullable=True,
               schema='my_app_schema')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('candidates', 'email',
               existing_type=sa.String(length=50),
               type_=sa.CHAR(length=50),
               existing_nullable=True,
               schema='my_app_schema')
    op.alter_column('candidates', 'phone',
               existing_type=sa.String(length=20),
               type_=sa.CHAR(length=20),
               existing_nullable=True,
               schema='my_app_schema')
    op.alter_column('candidates', 'candidate_name',
               existing_type=sa.String(length=50),
               type_=sa.CHAR(length=50),
               existing_nullable=False,
               schema='my_app_schema')
    # ### end Alembic commands ###