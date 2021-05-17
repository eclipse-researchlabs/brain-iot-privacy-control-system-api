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
from typing import Optional, Tuple

# Third Party
from fastapi import HTTPException, status
from httpx import HTTPStatusError, RequestError

# Internal
from .token import get_brain_pep_token
from ..logger import log_http_status_error, log_http_request_error
from ..session import get_keycloak_session
from ...config import get_brainpep_settings
from ...models.brain_pep.service import Service, get_service_id

# ------------------------------------------------------------------------------


async def _get_token_url(identifier: Optional[str] = None) -> Tuple[str, str]:
    """
    Get token and url to use with keycloak

    :param identifier: resource identifier
    :return: tuple with token and url
    """
    # Get settings and token
    settings = get_brainpep_settings()
    token = await get_brain_pep_token()

    if identifier:
        return token, f"{settings.resource_request_url}/{identifier}"
    return token, f"{settings.resource_request_url}"


async def insert_resource(resource: Service) -> str:
    """
    Insert resource on keycloak

    :param resource: resource to update
    :return: resource identifier on keycloak
    """
    # Get token and url
    token, url = await _get_token_url()
    connection = get_keycloak_session()

    try:
        # Update resource on keycloak
        response = await connection.post(
            url, json=resource.dict(), headers={"Authorization": f"Bearer {token}"}
        )
        try:
            response.raise_for_status()
            return get_service_id(response.content)
        except HTTPStatusError as error:
            await log_http_status_error(error, token)
            raise HTTPException(
                status_code=error.response.status_code, detail=str(repr(error))
            )
    except RequestError as error:
        # Something went wrong during the connection
        await log_http_request_error(error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Brain-Pep-Api service",
        )


async def update_resource(identifier: str, resource: Service) -> None:
    """
    Update resource from keycloak

    :param identifier: resource identifier
    :param resource: resource to update
    """
    # Get token and url
    token, url = await _get_token_url(identifier)
    connection = get_keycloak_session()

    try:
        # Update resource on keycloak
        response = await connection.put(
            url, json=resource.dict(), headers={"Authorization": f"Bearer {token}"}
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            await log_http_status_error(error, token)
            raise HTTPException(
                status_code=error.response.status_code, detail=str(repr(error))
            )
    except RequestError as error:
        # Something went wrong during the connection
        await log_http_request_error(error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Brain-Pep-Api service",
        )


async def delete_resource(identifier: str) -> None:
    """
    Delete resource from keycloak

    :param identifier: resource identifier
    """
    # Get token and url
    token, url = await _get_token_url(identifier)
    connection = get_keycloak_session()

    try:
        # Delete resource from keycloak
        response = await connection.delete(
            url, headers={"Authorization": f"Bearer {token}"}
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as error:
            await log_http_status_error(error, token)
            raise HTTPException(
                status_code=error.response.status_code, detail=str(repr(error))
            )
    except RequestError as error:
        # Something went wrong during the connection
        await log_http_request_error(error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Brain-Pep-Api service",
        )
