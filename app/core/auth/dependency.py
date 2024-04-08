import datetime

from fastapi import Depends, HTTPException

from app.core.auth.backend import fastapi_users_component
from app.db.tables import User

current_user = fastapi_users_component.current_user()


def authenticated_user(current_user: User = Depends(current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return current_user


def subscribed_user(current_user: User = Depends(current_user)):
    if (
        not current_user.subscription.expires_at > datetime.datetime.now()
        or not current_user.is_superuser
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


def artist_user(current_user: User = Depends(current_user)):
    if not current_user.is_artist:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


def superuser(current_user: User = Depends(current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user
