from fastapi import Depends

from app.core.auth.manager import UserManager
from app.db.dependency import get_user_db


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
