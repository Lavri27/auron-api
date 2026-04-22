"""add cover_path to tracks

Revision ID: 9c7c8a1d4e21
Revises: 4bbfaf7cf0fd
Create Date: 2026-04-22 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9c7c8a1d4e21"
down_revision: Union[str, None] = "4bbfaf7cf0fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("tracks", sa.Column("cover_path", sa.String(length=500), nullable=True))


def downgrade() -> None:
    op.drop_column("tracks", "cover_path")
