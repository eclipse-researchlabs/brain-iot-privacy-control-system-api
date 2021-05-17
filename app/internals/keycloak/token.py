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

# Third Party
from fastapi import status, HTTPException
from httpx import HTTPStatusError, RequestError

# Internal
from .constants import ADMIN_DATA, CLIENT_DATA
from ..session import get_keycloak_session
from ..logger import get_logger, log_http_status_error, log_http_request_error
from ...models.security import Token

# ----------------------------------------------------------------------------------


async def _get_token(url: str, data: dict) -> str:
    """
    Extract a Token from keycloak

    :param url: Url to use
    :param data: Data to insert
    """
    # Get Logger
    logger = get_logger()
    connection = get_keycloak_session()
    try:
        await logger.debug(url)
        response = await connection.post(
            url=url,
            data=data,
            timeout=25,
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as exc:
            await log_http_status_error(exc, data=data)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials"
            )
    except RequestError as exc:
        await log_http_request_error(exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Keycloak service",
        )

    return Token.parse_raw(response.content).access_token


async def get_admin_token() -> str:
    """
    Obtain a valid Administrator Token to communicate with BrainPep-Api

    :return: BrainPepApi valid token
    """
    return await _get_token(ADMIN_DATA["url"], ADMIN_DATA["data"])


async def get_brain_pep_token() -> str:
    """
    Obtain a valid Client Token to communicate with BrainPep-Api

    :return: BrainPepApi valid token
    """
    return await _get_token(CLIENT_DATA["url"], CLIENT_DATA["data"])
