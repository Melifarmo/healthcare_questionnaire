"""Application with configuration for events, routers and middleware."""
import os
from functools import partial
from typing import Any, Callable, Optional

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.routers import router
from app.db.sqlalchemy import close_db_connections
from app.settings import settings


async def startup() -> None:
    # -- Bot --
    ...
    # # -- Redis --
    # bot.state.redis = create_redis_client(max_connections=15)  # noqa: WPS432
    # bot.state.redis_repo = RedisRepo(
    #     redis=bot.state.redis, prefix=f"{BOT_PROJECT_NAME}:{settings.CONTAINER_PREFIX}"
    # )

    # # - Tasks -
    # if not os.environ.get("PYTEST_CURRENT_TEST"):
    #     await queue.enqueue(
    #         Job("update_companies_list", key="update_companies_list-startup"),
    #         timeout=settings.WORKER_TIMEOUT,
    #     )
    #
    #     async with db_session_factory() as session:
    #         await replace_base64_images_with_link(
    #             session, bot, settings.HOMESCREEN_BOT_CREDENTIALS[0].id
    #         )
    #         await session.commit()


async def shutdown() -> None:
    # -- Database --
    await close_db_connections()


def get_application(  # noqa: WPS213
    add_internal_error_handler: bool = True,
) -> FastAPI:
    """Create configured server application instance."""
    application = FastAPI(
        title='max',
        openapi_url="/openapi.json" if settings.DEBUG else None,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url=None,
    )
    origins = [
        "http://127.0.0.1:8000",  # Замените на адрес вашего фронтенда
        "http://localhost:8000",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Позволяет запросы с указанных источников
        allow_credentials=True,
        allow_methods=["*"],  # Позволяет все методы (GET, POST и т.д.)
        allow_headers=["*"],  # Позволяет все заголовки
    )

    application.add_event_handler("startup", partial(startup))
    application.add_event_handler("shutdown", partial(shutdown))

    application.include_router(router)

    # @application.middleware("http")
    # async def logger_middleware(  # noqa: WPS430
    #     request: Request, call_next: Callable
    # ) -> Response:
    #     if not request.url.path.startswith("/admin/api/") or not settings.DEBUG:
    #         return await call_next(request)
    #
    #     return await process_logging(request, call_next)

    # def get_custom_openapi() -> dict[str, Any]:  # noqa: WPS430
    #     return custom_openapi(
    #         title="Homescreen API",
    #         version=get_version(),
    #         fastapi_routes=application.routes,
    #         rpc_router=smartapp.router,
    #         openapi_version="3.0.2",
    #     )

    # application.openapi = get_custom_openapi  # type: ignore
    return application
