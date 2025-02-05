import datetime
import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from sqlalchemy import insert, update

from app.db.tables import Subscription, User


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = "SECRET"

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        """task: Automatically subscribe user to ticket plan after registration."""

        async with self.user_db.session as sess:
            insert_subscription_stmt = (
                insert(Subscription)
                .values(
                    name="ticket",
                    is_active=True,
                )
                .returning(Subscription)
            )
            subscription = (await sess.execute(insert_subscription_stmt)).scalar_one()

            update_user_subscription_stmt = (
                update(User)
                .where(User.id == user.id)
                .values(subscription_id=subscription.id)
            )

            await sess.execute(update_user_subscription_stmt)
            await sess.commit()
            await sess.refresh(user, ["subscription"])

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
