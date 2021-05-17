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
from typing import Optional

# Third Party
from fastapi import HTTPException, status
from fastuuid import uuid4
from httpx import HTTPStatusError, RequestError
from pydantic import ValidationError

# Internal
from ..logger import log_http_status_error, log_http_request_error
from ..session import get_keycloak_session
from ...config import get_brainpep_settings
from ...models.keycloak.attributes import Attributes

# ------------------------------------------------------------------------------


async def get_user_identifier(
    admin_token: str,
    keycloak_id: str,
) -> Optional[str]:
    """
    Extract user identifier from keycloak user's attributes

    :param admin_token: Administrator token
    :param keycloak_id: User identifier
    :return: Identifier of the attributes associated to the user
    """

    # Get settings
    settings = get_brainpep_settings()
    url = f"{settings.user_attribute_request_url}/{keycloak_id}"
    connection = get_keycloak_session()

    try:
        # Get user attributes
        response = await connection.get(
            f"{url}", headers={"Authorization": f"Bearer {admin_token}"}, timeout=10
        )
        try:
            # Check if the token is expired
            response.raise_for_status()
            try:
                return Attributes.parse_raw(
                    response.content
                ).attributes.device_policy_list
            except ValidationError:
                return None

        except HTTPStatusError as exc:
            await log_http_status_error(exc, admin_token)
            raise HTTPException(
                status_code=exc.response.status_code, detail=str(repr(exc))
            )

    except RequestError as exc:
        # Something went wrong during the connection
        await log_http_request_error(exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Brain-Pep-Api service",
        )


async def set_user_identifier(admin_token: str, user_id: str) -> str:
    """
    Set an identifier  for the user in keycloak

    :param admin_token: Administrator token
    :param user_id: User Identifier
    :return: keycloak identifier
    """

    # Get settings
    settings = get_brainpep_settings()
    connection = get_keycloak_session()

    # Extract url
    url = f"{settings.user_attribute_request_url}/{user_id}"
    # Generate identifier
    identifier = str(uuid4())

    try:
        response = await connection.put(
            url,
            json={"attributes": {"device_policy_list": identifier}},
            headers={"Authorization": f"Bearer {admin_token}"},
            timeout=10,
        )
        try:
            # Check if everything is ok
            response.raise_for_status()
            return identifier

        except HTTPStatusError as exc:
            await log_http_status_error(exc, admin_token)
            raise HTTPException(
                status_code=exc.response.status_code, detail=str(repr(exc))
            )

    except RequestError as exc:
        # Something went wrong during the connection
        await log_http_request_error(exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Brain-Pep-Api service",
        )
