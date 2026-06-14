"""add lesson_progress table

세션(레슨) 수강 완료 추적 도메인. (user_id, lesson_id) 당 1 row.

Revision ID: add_lesson_progress_001
Revises: drop_uq_user_lecture_001
Create Date: 2026-06-14

"""

from alembic import op
import sqlalchemy as sa

revision = "add_lesson_progress_001"
down_revision = "drop_uq_user_lecture_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("lesson_id", sa.Integer(), nullable=False),
        sa.Column("lecture_id", sa.Integer(), nullable=False),
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["lesson_id"], ["lesson.id"]),
        sa.ForeignKeyConstraint(["lecture_id"], ["lecture.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "lesson_id", name="uq_user_lesson_progress"
        ),
    )
    op.execute("ALTER TABLE lesson_progress ENABLE ROW LEVEL SECURITY;")


def downgrade() -> None:
    op.drop_table("lesson_progress")
