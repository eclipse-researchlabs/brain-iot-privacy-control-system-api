"""

:author: Angelo Cutaia
*******************************************************************************
* Copyright (C) 2021 LINKS Foundation
*
* This program and the accompanying materials are made
* available under the terms of the Eclipse Public License 2.0
* which is available at https://www.eclipse.org/legal/epl-2.0/
*
* SPDX-License-Identifier: EPL-2.0
 ******************************************************************************
"""
# Standard Library
import logging
from functools import lru_cache
from typing import Optional

# Third Party
from aiologger.loggers.json import JsonLogger, Logger, LogLevel
from asyncpg import PostgresError
from httpx import HTTPStatusError, RequestError
from pydantic import BaseSettings

# ---------------------------------------------------------------------


class LoggerSettings(BaseSettings):
    log_level: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_logger() -> Logger:
    """Instantiate app logger"""
    settings = LoggerSettings()
    # Configure uvicorn logger
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.setLevel(settings.log_level)
    return JsonLogger.with_default_handlers(
        name="serengeti",
        level=getattr(LogLevel, settings.log_level, LogLevel.DEBUG),
        serializer_kwargs={"indent": 4},
    )


async def log_http_status_error(
    error: HTTPStatusError, token: Optional[str] = None, data: Optional[dict] = None
):
    """
    Log the http status error

    :param error: http exception
    :param token: token associated to the request
    :param data: data associated to the request
    """
    logger = get_logger()
    request = {
        "method": error.request.method,
        "url": error.request.url,
        "status_code": error.response.status_code,
        "error": str(repr(error)),
    }
    if token and data is None:
        request.update({"token": token})
        await logger.warning(request)
    elif data:
        request.update({"credential": data})
        await logger.error(request)


async def log_http_request_error(error: RequestError):
    """
    Log the http status error

    :param error: http exception
    """
    logger = get_logger()
    await logger.error(
        {
            "method": error.request.method,
            "url": error.request.url,
            "error": str(repr(error)),
        }
    )


async def log_postgres_error(error: PostgresError):
    """
    Log the Postgres error

    :param error: postgres exception
    """
    logger = get_logger()
    await logger.warning(error.as_dict())
