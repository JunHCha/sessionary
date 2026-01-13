"""add ticket_usage table

Revision ID: add_ticket_usage_001
Revises: enable_rls_001
Create Date: 2026-01-13 23:00:00

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "add_ticket_usage_001"
down_revision = "enable_rls_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ticket_usage",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("lecture_id", sa.Integer(), nullable=False),
        sa.Column(
            "used_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["lecture_id"],
            ["lecture.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "lecture_id", name="uq_user_lecture"),
    )
    op.execute("ALTER TABLE ticket_usage ENABLE ROW LEVEL SECURITY;")


def downgrade() -> None:
    op.drop_table("ticket_usage")
