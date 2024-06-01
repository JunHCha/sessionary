from logging.config import fileConfig

from alembic import context
from pydantic import PostgresDsn
from sqlalchemy import pool
from sqlalchemy.engine import engine_from_config

from app.core.settings.base import AppEnv
from app.depends.settings import get_app_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.


def get_psycopg_url(database_url: PostgresDsn) -> str:
    return str(database_url).replace("postgresql+asyncpg://", "postgresql://")


settings = get_app_settings()
db_url = get_psycopg_url(settings.database_url)


config = context.config
if settings.app_env == AppEnv.dev:
    fileConfig(config.config_file_name)


from app.db import tables  # noqa

target_metadata = tables.Base.metadata

config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
