"""Managers dependencies."""
from typing import Generator

from fastapi import Depends, HTTPException
from pybotx import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_502_BAD_GATEWAY

from app.api.dependencies.bot import get_bot_depends
from app.api.dependencies.db_session import get_session
from app.logger import logger
from app.schemas.news.rss import RSSBaseError, RSSNoNewsError
from app.services.managers.adverts_manager import AdvertsManager
from app.services.managers.news_manager import NewsManager
from app.services.managers.rss_manager import RSSManager
from app.services.strategies.image_delivery import AdminStaticImageDeliveryStrategy


def get_news_manager(
    bot: Bot = Depends(get_bot_depends), db_session: AsyncSession = Depends(get_session)
) -> NewsManager:
    return NewsManager(
        db_session,
        bot,
        AdminStaticImageDeliveryStrategy(db_session=db_session),
    )


def get_rss_manager(bot: Bot = Depends(get_bot_depends)) -> RSSManager:
    return RSSManager(bot.state.redis_repo)


def get_advert_manager(
    db_session: AsyncSession = Depends(get_session),
) -> AdvertsManager:
    return AdvertsManager(
        db_session,
        AdminStaticImageDeliveryStrategy(db_session=db_session),
    )


def handle_rss_error() -> Generator[None, None, None]:
    try:
        yield
    except RSSNoNewsError as exc:
        logger.opt(exception=exc).error(str(exc))
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=str(exc.msg)  # noqa: WPS432
        ) from exc
    except RSSBaseError as exc:
        logger.opt(exception=exc).error(str(exc))
        raise HTTPException(
            status_code=HTTP_502_BAD_GATEWAY, detail=str(exc.msg)
        ) from exc
