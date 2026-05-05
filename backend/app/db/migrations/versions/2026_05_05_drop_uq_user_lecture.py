"""drop uq_user_lecture unique constraint from ticket_usage

ticket_usage는 티켓 사용 로그 테이블이므로 같은 (user_id, lecture_id)에 대해
여러 row가 허용되어야 한다. 기존 unique constraint는 설계 오류.

Revision ID: drop_uq_user_lecture_001
Revises: add_session_fields_001
Create Date: 2026-05-05

"""

from alembic import op

revision = "drop_uq_user_lecture_001"
down_revision = "add_session_fields_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("uq_user_lecture", "ticket_usage", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint("uq_user_lecture", "ticket_usage", ["user_id", "lecture_id"])
