import datetime

from fastapi import Depends, HTTPException

from app.db.tables import User


async def current_user_placeholder():
    raise NotImplementedError("current_user dependency should be overridden")


def authenticated_user(user: User = Depends(current_user_placeholder)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return user


def subscribed_user(user: User = Depends(current_user_placeholder)):
    if not user.is_superuser:
        if not user.subscription_id:
            raise HTTPException(status_code=403, detail="No subscription found")

        if user.expires_at and user.expires_at < datetime.datetime.now():
            raise HTTPException(status_code=403, detail="Subscription expired")

        if user.ticket_count <= 0:
            raise HTTPException(status_code=403, detail="No tickets available")
    return user


def artist_user(user: User = Depends(current_user_placeholder)):
    if not (user.is_artist or user.is_superuser):
        raise HTTPException(status_code=403, detail="Forbidden")
    return user


def superuser(user: User = Depends(current_user_placeholder)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user
