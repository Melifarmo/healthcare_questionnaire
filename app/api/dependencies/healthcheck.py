"""Bot dependency for healthcheck."""
from asyncio.exceptions import TimeoutError
from typing import Optional

from fastapi import Request
from pybotx import Bot
from sqlalchemy import text

from app.db.sqlalchemy import db_session_factory
from app.settings import settings
from app.worker.worker import queue


async def check_db_connection(request: Request) -> Optional[str]:
    assert isinstance(request.app.state.bot, Bot)

    async with db_session_factory() as db_session:
        try:
            await db_session.execute(text("SELECT 1"))
        except Exception as exc:
            return str(exc)

    return None


async def check_redis_connection(request: Request) -> Optional[str]:
    assert isinstance(request.app.state.bot, Bot)

    bot = request.app.state.bot
    return await bot.state.redis_repo.ping()


async def check_worker_status() -> Optional[str]:
    job = await queue.enqueue("healthcheck")

    try:
        await job.refresh(settings.HEALTHCHECK_WORKER_TIMEOUT_SEC)  # type: ignore
    except TimeoutError:
        return "Worker is overloaded or not launched"
    except Exception as exc:
        return str(exc)

    return None
