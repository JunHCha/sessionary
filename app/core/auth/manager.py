import uuid
from typing import Any, Optional

from fastapi import Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.db.tables import User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = "SECRET"

    async def on_after_register(
        self, user: Any, request: Request | None = None
    ) -> None:
        # TODO: Auto subscription to free plan
        pass

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        # TODO: Make subscription session
        pass

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
