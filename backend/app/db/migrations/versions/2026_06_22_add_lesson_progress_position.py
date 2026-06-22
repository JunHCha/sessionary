"""add partial-progress fields to lesson_progress

부분 진행도(이어보기 위치/영상 길이/누적 시청률) + 미완료 행 허용(completed_at nullable).

Revision ID: add_progress_position_001
Revises: convert_subtitle_ts_001
Create Date: 2026-06-22

"""

from alembic import op
import sqlalchemy as sa

revision = "add_progress_position_001"
down_revision = "convert_subtitle_ts_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("lesson_progress") as batch_op:
        batch_op.add_column(
            sa.Column(
                "last_position_sec",
                sa.Integer(),
                server_default="0",
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column("duration_sec", sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "progress_percent",
                sa.Integer(),
                server_default="0",
                nullable=False,
            )
        )
        batch_op.alter_column(
            "completed_at",
            existing_type=sa.DateTime(timezone=True),
            nullable=True,
            server_default=None,
        )


def downgrade() -> None:
    with op.batch_alter_table("lesson_progress") as batch_op:
        batch_op.alter_column(
            "completed_at",
            existing_type=sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        )
        batch_op.drop_column("progress_percent")
        batch_op.drop_column("duration_sec")
        batch_op.drop_column("last_position_sec")
