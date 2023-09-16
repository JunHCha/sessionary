from app.core.auth.backend import fastapi_users_component


async def get_current_user():
    yield fastapi_users_component.current_user()
