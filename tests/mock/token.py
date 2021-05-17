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
from enum import Enum

# Third Party
from fastapi import status
from httpx import Response
import respx

# Internal
from app.internals.keycloak.constants import ADMIN_DATA, CLIENT_DATA

# ----------------------------------------------------------------------------------


class TokenType(str, Enum):
    client = "client"
    admin = "admin"


def correct_get_token(token_type: TokenType, token: str):
    """
    Mocked get iota user

    :param token_type: Must be client or user
    :param token: Mocked result token
    """

    if token_type == TokenType.admin:
        respx.post(ADMIN_DATA["url"]).mock(
            return_value=Response(
                status_code=status.HTTP_200_OK, json={"access_token": token}
            )
        )
    else:
        respx.post(CLIENT_DATA["url"]).mock(
            return_value=Response(
                status_code=status.HTTP_200_OK, json={"access_token": token}
            )
        )


def error_get_token(token_type: TokenType):
    """
    Mocked get iota user

    :param token_type: Must be client or user
    """

    if token_type == TokenType.admin:
        respx.post(ADMIN_DATA["url"]).mock(
            return_value=Response(status_code=status.HTTP_404_NOT_FOUND)
        )
    else:
        respx.post(CLIENT_DATA["url"]).mock(
            return_value=Response(status_code=status.HTTP_404_NOT_FOUND)
        )
