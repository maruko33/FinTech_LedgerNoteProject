import asyncio
from logging.config import fileConfig
import os

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from db.base import Base
target_metadata = Base.metadata


def _get_db_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url

    # fallback to alembic.ini (optional but helpful)
    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url and "driver://user:pass@localhost/dbname" not in ini_url:
        return ini_url

    raise RuntimeError(
        "DATABASE_URL is not set. Set it in your environment or .env file."
    )


def run_migrations_offline() -> None:
    url = _get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    db_url = _get_db_url()
    connectable = create_async_engine(db_url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
