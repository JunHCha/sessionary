import datetime
import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions, models, schemas
from sqlalchemy import insert

from app.db.dependency import get_session
from app.db.tables import Subscription, User, UserXSubscription


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = "SECRET"

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Request | None = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        # query again to get the full user with subscriptions
        async for sess in get_session():
            user = await sess.get(User, created_user.id)

        return user

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        """task: Automatically subscribe user to ticket plan after registration."""

        async for sess in get_session():
            insert_subscription_stmt = (
                insert(Subscription)
                .values(
                    name="ticket",
                    is_active=True,
                    ticket_count=3,
                    expires_at=datetime.datetime.now().replace(year=9999),
                )
                .returning(Subscription)
            )
            subscription = (await sess.execute(insert_subscription_stmt)).scalar_one()
            insert_association_stmt = insert(UserXSubscription).values(
                user_id=user.id, subscription_id=subscription.id
            )
            await sess.execute(insert_association_stmt)
            await sess.commit()

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
