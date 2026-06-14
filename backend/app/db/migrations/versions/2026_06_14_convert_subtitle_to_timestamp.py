"""convert lesson subtitles from start/end to timestamp_ms

옛 자막 형식 {start, end, text} 를 현재 Subtitle 스키마 {timestamp_ms, text} 로
변환한다. timestamp_ms 는 기존 start(ms) 값을 사용하고 end 는 폐기한다.

배경: Subtitle 모델은 timestamp_ms 기반인데, 일부 환경(staging 등)의
lesson.subtitles 데이터가 옛 start/end 형식으로 남아 있어 세션 상세 응답이
Subtitle 검증에서 실패(500)한다. 이 데이터 마이그레이션으로 형식을 일치시킨다.

PostgreSQL 전용(jsonb 함수 사용). 이미 timestamp_ms 형식인 row 는 건너뛰므로
재실행해도 안전(idempotent)하다.

Revision ID: convert_subtitle_ts_001
Revises: add_lesson_progress_001
Create Date: 2026-06-14

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "convert_subtitle_ts_001"
down_revision = "add_lesson_progress_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE lesson
        SET subtitles = (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'timestamp_ms',
                    COALESCE((e->>'start')::int, (e->>'timestamp_ms')::int, 0),
                    'text', e->>'text'
                )
                ORDER BY ord
            )
            FROM jsonb_array_elements(subtitles::jsonb) WITH ORDINALITY AS t(e, ord)
        )::json
        WHERE subtitles IS NOT NULL
          AND jsonb_typeof(subtitles::jsonb) = 'array'
          AND jsonb_array_length(subtitles::jsonb) > 0
          AND NOT (subtitles::jsonb -> 0 ? 'timestamp_ms');
        """
    )


def downgrade() -> None:
    # 비가역: timestamp_ms 만으로 원래 start/end 분할을 복구할 수 없다.
    # 데이터 정합성 보정 마이그레이션이므로 downgrade 는 의도적으로 no-op.
    pass
