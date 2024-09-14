from asyncio import current_task
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings

from typing import Callable

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool.impl import AsyncAdaptedQueuePool

from app.settings import settings

AsyncSessionFactory = Callable[..., AsyncSession]


def make_url_async(url: str) -> str:
    """Add +asyncpg to url scheme."""
    return "postgresql+asyncpg" + url[url.find(":") :]  # noqa: WPS336


def make_url_sync(url: str) -> str:
    """Remove +asyncpg from url scheme."""
    return "postgresql" + url[url.find(":") :]  # noqa: WPS336


Base = declarative_base(metadata=MetaData())

engine: AsyncEngine = create_async_engine(
    make_url_async(settings.POSTGRES_DSN), poolclass=AsyncAdaptedQueuePool
)

db_session_factory = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def build_db_session_factory() -> AsyncSessionFactory:
    await verify_db_connection(engine)

    return async_scoped_session(
        async_sessionmaker(bind=engine, expire_on_commit=False),
        scopefunc=current_task,
    )


async def verify_db_connection(engine: AsyncEngine) -> None:
    connection = await engine.connect()
    await connection.close()


async def close_db_connections() -> None:
    await engine.dispose()
