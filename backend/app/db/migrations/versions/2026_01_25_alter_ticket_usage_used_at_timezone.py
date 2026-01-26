"""alter ticket_usage used_at to use timezone

Revision ID: alter_ticket_usage_002
Revises: add_ticket_usage_001
Create Date: 2026-01-25 12:00:00

"""

from alembic import op

revision = "alter_ticket_usage_002"
down_revision = "add_ticket_usage_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE ticket_usage ALTER COLUMN used_at TYPE TIMESTAMP WITH TIME ZONE"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE ticket_usage ALTER COLUMN used_at TYPE TIMESTAMP WITHOUT TIME ZONE"
    )
