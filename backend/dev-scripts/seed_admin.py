"""로컬 QA용 admin(is_superuser) 계정 시드 스크립트.

Google OAuth 없이 admin 페이지를 QA하기 위한 용도. **dev 환경에서만** 동작한다.

    cd backend && APP_ENV=dev uv run python dev-scripts/seed_admin.py

자격증명은 환경변수로 덮어쓸 수 있다(미지정 시 로컬 dev 기본값 사용):

    SEED_ADMIN_EMAIL=me@example.com SEED_ADMIN_PASSWORD=... \
        APP_ENV=dev uv run python dev-scripts/seed_admin.py

생성 후 브라우저 콘솔(http://localhost:5173)에서 아래로 로그인하면 세션 쿠키가 설정된다.

    await fetch('http://localhost:8000/user/auth/login', {
      method: 'POST', credentials: 'include',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'username=admin@sessionary.com&password=admin1234'
    })

보안: 이 스크립트는 공개 레포에 포함되므로 superuser 계정을 임의 환경에 만들지 않도록
APP_ENV != dev 이면 즉시 중단한다. 하드코딩된 기본 비밀번호는 로컬 dev 전용이다.
"""

import asyncio
import os

from fastapi_users.schemas import BaseUserCreate
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.auth.manager import UserManager
from app.containers.application import ApplicationContainer
from app.core.settings.base import AppEnv
from app.db.tables import OAuthAccount, User

DEFAULT_EMAIL = "admin@sessionary.com"
DEFAULT_PASSWORD = "admin1234"


async def main() -> None:
    container = ApplicationContainer()
    settings = container.settings()
    if settings.app_env != AppEnv.dev:
        raise SystemExit(
            f"[seed_admin] dev 환경에서만 실행할 수 있습니다 (현재 APP_ENV={settings.app_env.value}). "
            "스테이징/프로덕션에는 절대 admin 계정을 이 스크립트로 만들지 마세요."
        )

    email = os.environ.get("SEED_ADMIN_EMAIL", DEFAULT_EMAIL)
    password = os.environ.get("SEED_ADMIN_PASSWORD", DEFAULT_PASSWORD)

    session_manager = container.database.session_manager()
    async with session_manager.async_session() as session:
        user_db = SQLAlchemyUserDatabase(session, User, OAuthAccount)
        manager = UserManager(user_db)

        existing = await user_db.get_by_email(email)
        if existing is not None:
            existing.is_superuser = True
            existing.is_active = True
            existing.is_verified = True
            await session.commit()
            print(f"[seed_admin] 기존 계정을 admin으로 갱신: {email} (id={existing.id})")
        else:
            user = await manager.create(
                BaseUserCreate(
                    email=email,
                    password=password,
                    is_superuser=True,
                    is_active=True,
                    is_verified=True,
                )
            )
            print(f"[seed_admin] admin 생성: {email} (id={user.id})")


if __name__ == "__main__":
    asyncio.run(main())
