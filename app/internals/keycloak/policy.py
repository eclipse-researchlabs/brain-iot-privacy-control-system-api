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
from typing import Optional, List

# Third Party
from fastapi import HTTPException, status
from httpx import HTTPStatusError, RequestError

# Internal
from .token import get_admin_token
from ..logger import log_http_status_error, log_http_request_error
from ..session import get_keycloak_session
from ...config import get_brainpep_settings
from ...models.keycloak.role import parse_roles

# ------------------------------------------------------------------------------


async def get_available_policies(admin_token: Optional[str] = None) -> List[str]:
    """
    Extract a Policies from BrainPep-API

    :param admin_token: Administrator token
    :return: Policies
    """

    # Get settings
    settings = get_brainpep_settings()
    client = get_keycloak_session()

    # If no token is give, extract it
    if admin_token is None:
        admin_token = await get_admin_token()

    try:
        response = await client.get(
            settings.policy_request_url,
            headers={"Authorization": f"Bearer {admin_token}"},
            timeout=10,
        )
        try:
            # Check if the token is expired
            response.raise_for_status()
            return parse_roles(response.content)

        except HTTPStatusError as error:
            await log_http_status_error(error, admin_token)

    except RequestError as error:
        # Something went wrong during the connection
        await log_http_request_error(error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't contact Keycloak service",
        )
