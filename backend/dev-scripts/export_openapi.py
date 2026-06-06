"""OpenAPI 스펙을 backend/openapi.json 스냅샷으로 export 한다.

이 스냅샷이 프론트엔드 API client(openapi-ts) 생성의 단일 진실 소스다.
백엔드를 띄우지 않고 app 객체에서 직접 스펙을 뽑으므로 DB/네트워크 의존이 없다.

사용법:
    uv run python dev-scripts/export_openapi.py
    uv run python dev-scripts/export_openapi.py --check   # 재생성 후 diff 없으면 0, 있으면 1

`--check` 는 CI 에서 "백엔드 코드와 커밋된 스펙이 동기화되어 있는가"를 검증한다.
"""

from __future__ import annotations

import argparse
import json
from os import environ
from pathlib import Path
import sys

# app 객체만 생성하면 되므로 DB 연결이 필요 없는 test 설정을 사용한다.
# (TestAppSettings 가 모든 required 필드에 기본값을 제공)
environ.setdefault("APP_ENV", "test")

from app.main import get_application  # noqa: E402

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "openapi.json"


def build_spec() -> str:
    app = get_application()
    spec = app.openapi()
    # FastAPI 의 출력은 코드 정의 순서를 따르는 결정적 순서다. 일부러 정렬하지
    # 않아(sort_keys=False) 라이브 스펙과 동일한 순서를 유지하고, client 도 그
    # 순서대로 생성되어 무의미한 대량 diff 를 피한다. trailing newline 만 보장한다.
    return json.dumps(spec, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export OpenAPI spec snapshot")
    parser.add_argument(
        "--check",
        action="store_true",
        help="재생성 결과가 커밋된 파일과 다르면 비정상 종료(1)",
    )
    args = parser.parse_args()

    spec = build_spec()

    if args.check:
        if not OUTPUT_PATH.exists():
            print(f"[export_openapi] {OUTPUT_PATH} 가 없습니다. 먼저 생성하세요.")
            return 1
        current = OUTPUT_PATH.read_text(encoding="utf-8")
        if current != spec:
            print(
                "[export_openapi] openapi.json 이 백엔드 코드와 다릅니다. "
                "`uv run python dev-scripts/export_openapi.py` 후 커밋하세요."
            )
            return 1
        print("[export_openapi] openapi.json 동기화 확인됨.")
        return 0

    OUTPUT_PATH.write_text(spec, encoding="utf-8")
    print(f"[export_openapi] {OUTPUT_PATH} 생성 완료.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
