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
from fastapi import status
from httpx import Response
import respx

# Internal
from app.config import get_brainpep_settings
from .token import correct_get_token, TokenType

# ----------------------------------------------------------------------------------


def _keycloak_url(keycloak_id: str) -> str:
    """
    Generate the url to mock

    :param keycloak_id: user identifier
    :return: url to mock
    """
    correct_get_token(TokenType.admin, "fake_admin_token")
    settings = get_brainpep_settings()
    return f"{settings.user_attribute_request_url}/{keycloak_id}"


def correct_get_user_identifier(keycloak_id: str, requested_id: str):
    """
    Mock the interaction with keycloak

    :param keycloak_id: user identifier
    :param requested_id: identifier of the items that internally are stored in the table device_mapping
    """
    url = _keycloak_url(keycloak_id)
    respx.get(url).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json={"attributes": {"device_policy_list": [requested_id]}},
        )
    )


def correct_set_user_identifier(keycloak_id: str):
    """
    Mock the interaction with keycloak

    :param keycloak_id: user identifier
    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _keycloak_url(keycloak_id)
    respx.put(url).mock(return_value=Response(status_code=status.HTTP_200_OK))


def error_get_user_identifier(keycloak_id: str):
    """
    Mock the interaction with keycloak

    :param keycloak_id: user identifier
    """
    url = _keycloak_url(keycloak_id)
    respx.get(url).mock(return_value=Response(status_code=status.HTTP_404_NOT_FOUND))


def error_set_user_identifier(keycloak_id: str):
    """
    Mock the interaction with keycloak

    :param keycloak_id: user identifier
    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _keycloak_url(keycloak_id)
    respx.put(url).mock(return_value=Response(status_code=status.HTTP_404_NOT_FOUND))
