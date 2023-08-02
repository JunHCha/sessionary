from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import engine_from_config

from app.core.config import get_app_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

SETTINGS = get_app_settings()
DATABASE_URL = SETTINGS.database_url

config = context.config
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from app.db import tables  # noqa

target_metadata = tables.Base.metadata

config.set_main_option("sqlalchemy.url", str(DATABASE_URL))


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
