import uuid
from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from sqlalchemy import insert, update

from app.db.tables import Group, Subscription, User, UserSubscriptionHistory


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = "SECRET"

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        """Automatically subscribe user to ticket plan after registration."""

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
            # Create a group for the user
            insert_group_stmt = (
                insert(Group)
                .values(
                    name=f"user_{user.id}_group",
                    main_user_id=True,
                )
                .returning(Group)
            )
            group = (await sess.execute(insert_group_stmt)).scalar_one()
            # Update user with group_id
            update_user_group_stmt = (
                update(User).where(User.id == user.id).values(group_id=group.id)
            )
            await sess.execute(update_user_group_stmt)
            # Create subscription history record
            insert_history_stmt = insert(UserSubscriptionHistory).values(
                user_id=user.id,
                subscription_id=subscription.id,
                group_id=group.id,
            )
            await sess.execute(insert_history_stmt)
            await sess.commit()
            await sess.refresh(user, ["subscription"])

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
