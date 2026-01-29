"""add session fields to lesson table

Revision ID: add_session_fields_001
Revises: alter_ticket_usage_002
Create Date: 2026-01-27

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "add_session_fields_001"
down_revision = "alter_ticket_usage_002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    sessiontype_enum = postgresql.ENUM(
        "PLAY", "TALK", "JAM", "BASIC", "SHEET",
        name="sessiontype",
        create_type=True,
    )
    sessiontype_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "lesson",
        sa.Column("session_type", sessiontype_enum, nullable=True),
    )
    op.add_column(
        "lesson",
        sa.Column("subtitles", sa.JSON(), nullable=True),
    )
    op.add_column(
        "lesson",
        sa.Column("playing_guide", sa.JSON(), nullable=True),
    )
    op.add_column(
        "lesson",
        sa.Column("sync_offset", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("lesson", "sync_offset")
    op.drop_column("lesson", "playing_guide")
    op.drop_column("lesson", "subtitles")
    op.drop_column("lesson", "session_type")

    sessiontype_enum = postgresql.ENUM(
        "PLAY", "TALK", "JAM", "BASIC", "SHEET",
        name="sessiontype",
    )
    sessiontype_enum.drop(op.get_bind(), checkfirst=True)
