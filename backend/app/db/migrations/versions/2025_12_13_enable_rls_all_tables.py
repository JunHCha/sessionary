"""enable_rls_all_tables

Revision ID: enable_rls_001
Revises: 419db5652ed1
Create Date: 2025-12-13

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "enable_rls_001"
down_revision = "419db5652ed1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 모든 테이블에 RLS 활성화 (postgres superuser는 자동 우회됨)
    tables = [
        "oauth_account",
        '"user"',
        "subscription",
        '"group"',
        "user_subscription_history",
        "lecture",
        "playlist",
        "lesson",
        "playlist_x_lesson",
        "alembic_version",
    ]

    for table in tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")


def downgrade() -> None:
    tables = [
        "oauth_account",
        '"user"',
        "subscription",
        '"group"',
        "user_subscription_history",
        "lecture",
        "playlist",
        "lesson",
        "playlist_x_lesson",
        "alembic_version",
    ]

    for table in tables:
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")

