from app.core.fastapi_users_config.backend import fastapi_users_components


async def get_current_user():
    yield fastapi_users_components.current_user()
