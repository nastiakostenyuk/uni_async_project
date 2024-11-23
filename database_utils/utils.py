"""Set up the database connection and session.""" ""
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


from database_utils.models import Base
from settings import async_session, async_engine


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """Get a database session.

    To be used for dependency injection.
    """
    async with async_session() as session, session.begin():
        yield session


async def check_connection_to_db() -> None:
    """
    Function to check the connection to the database.
    :raises Exception: If an error occurs while connecting to the database
    :return: None
    """
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exp:
        raise Exception(f"Error while connecting to the database: {exp}")


async def init_models() -> None:
    """Create tables if they don't already exist.

    In a real-life example we would use Alembic to manage migrations.
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as exp:
        raise Exception(f"Error while creating tables: {exp}")
