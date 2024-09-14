"""Bot dependency for FastAPI."""

from fastapi import Request
from pybotx import Bot


def get_bot_depends(request: Request) -> Bot:
    assert isinstance(request.app.state.bot, Bot)

    return request.app.state.bot
