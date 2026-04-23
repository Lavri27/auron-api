"""add author role and track publish fields

Revision ID: b9f1e7d4c201
Revises: 9c7c8a1d4e21
Create Date: 2026-04-23 12:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b9f1e7d4c201"
down_revision: Union[str, None] = "9c7c8a1d4e21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("is_author", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("artists", sa.Column("owner_user_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_artists_owner_user_id"), "artists", ["owner_user_id"], unique=False)
    op.create_foreign_key(
        "fk_artists_owner_user_id_users",
        "artists",
        "users",
        ["owner_user_id"],
        ["id"],
    )

    op.add_column("tracks", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("tracks", sa.Column("genre", sa.String(length=100), nullable=True))
    op.create_index(op.f("ix_tracks_genre"), "tracks", ["genre"], unique=False)
    op.add_column("tracks", sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.false()))

    op.execute("UPDATE users SET is_author = false WHERE is_author IS NULL")
    op.execute("UPDATE tracks SET is_published = is_public")

    op.alter_column("users", "is_author", server_default=None)
    op.alter_column("tracks", "is_published", server_default=None)


def downgrade() -> None:
    op.drop_column("tracks", "is_published")
    op.drop_index(op.f("ix_tracks_genre"), table_name="tracks")
    op.drop_column("tracks", "genre")
    op.drop_column("tracks", "description")

    op.drop_constraint("fk_artists_owner_user_id_users", "artists", type_="foreignkey")
    op.drop_index(op.f("ix_artists_owner_user_id"), table_name="artists")
    op.drop_column("artists", "owner_user_id")

    op.drop_column("users", "is_author")
