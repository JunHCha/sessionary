import datetime

from fastapi import Depends, HTTPException

from app.core.auth.backend import auth_backend
from app.db.tables import User

current_user = auth_backend.components.current_user()


def authenticated_user(current_user: User = Depends(current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return current_user


def subscribed_user(current_user: User = Depends(current_user)):
    if not current_user.is_superuser:
        # Check if user has active subscription
        if not current_user.subscription_id:
            raise HTTPException(
                status_code=403, detail="No subscription found"
            )

        # Check if subscription is expired
        if (
            current_user.expires_at
            and current_user.expires_at < datetime.datetime.now()
        ):
            raise HTTPException(
                status_code=403, detail="Subscription expired"
            )

        # Check if user has tickets
        if current_user.ticket_count <= 0:
            raise HTTPException(
                status_code=403, detail="No tickets available"
            )
    return current_user


def artist_user(current_user: User = Depends(current_user)):
    if not (current_user.is_artist or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


def superuser(current_user: User = Depends(current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user
