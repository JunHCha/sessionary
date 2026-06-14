"""add home_curation table

홈 화면 큐레이션 선정을 위한 home_curation 테이블 + curationsection enum 생성.

Revision ID: add_home_curation_001
Revises: drop_uq_user_lecture_001
Create Date: 2026-06-14

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "add_home_curation_001"
down_revision = "drop_uq_user_lecture_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    curationsection_enum = postgresql.ENUM(
        "TRENDING",
        "NEW",
        name="curationsection",
        create_type=True,
    )
    curationsection_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "home_curation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("section", curationsection_enum, nullable=False),
        sa.Column("lecture_id", sa.Integer(), nullable=False),
        sa.Column("ordering", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["lecture_id"], ["lecture.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("home_curation")

    curationsection_enum = postgresql.ENUM(
        "TRENDING",
        "NEW",
        name="curationsection",
    )
    curationsection_enum.drop(op.get_bind(), checkfirst=True)
