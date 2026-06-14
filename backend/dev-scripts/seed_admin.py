"""로컬 QA용 admin(is_superuser) 계정 시드 스크립트.

Google OAuth 없이 admin 페이지를 QA하기 위한 용도. APP_ENV=dev 로 실행한다.

    cd backend && APP_ENV=dev uv run python dev-scripts/seed_admin.py

생성 후 브라우저 콘솔(http://localhost:5173)에서 아래로 로그인하면 세션 쿠키가 설정된다.

    await fetch('http://localhost:8000/user/auth/login', {
      method: 'POST', credentials: 'include',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: 'username=admin@sessionary.com&password=admin1234'
    })
"""

import asyncio

from fastapi_users.schemas import BaseUserCreate
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.auth.manager import UserManager
from app.containers.application import ApplicationContainer
from app.db.tables import OAuthAccount, User

EMAIL = "admin@sessionary.com"
PASSWORD = "admin1234"


async def main() -> None:
    container = ApplicationContainer()
    session_manager = container.database.session_manager()
    async with session_manager.async_session() as session:
        user_db = SQLAlchemyUserDatabase(session, User, OAuthAccount)
        manager = UserManager(user_db)

        existing = await user_db.get_by_email(EMAIL)
        if existing is not None:
            existing.is_superuser = True
            existing.is_active = True
            existing.is_verified = True
            await session.commit()
            print(f"[seed_admin] 기존 계정을 admin으로 갱신: {EMAIL} (id={existing.id})")
        else:
            user = await manager.create(
                BaseUserCreate(
                    email=EMAIL,
                    password=PASSWORD,
                    is_superuser=True,
                    is_active=True,
                    is_verified=True,
                )
            )
            print(f"[seed_admin] admin 생성: {EMAIL} / {PASSWORD} (id={user.id})")


if __name__ == "__main__":
    asyncio.run(main())
