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
from fastapi import status
from httpx import Response
import respx

# Internal
from app.config import get_brainpep_settings
from .token import correct_get_token, TokenType

# ----------------------------------------------------------------------------------


def _extract_url(identifier: Optional[str] = None) -> str:
    """
    Extract url for mocking the request

    :param identifier: identifier of the resource
    :return: url
    """
    # Get settings and token
    settings = get_brainpep_settings()
    if identifier:
        return f"{settings.resource_request_url}/{identifier}"
    return settings.resource_request_url


def correct_insert_resource(identifier_to_return: str):
    """
    Mock the request

    :param identifier_to_return: Identifier that the request must return
    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _extract_url()
    respx.post(url).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK, json={"_id": identifier_to_return}
        )
    )


def correct_update_resource(identifier: str):
    """
    Mock the request

    :param identifier: identifier of the resource to update
    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _extract_url(identifier)
    respx.put(url).mock(return_value=Response(status_code=status.HTTP_200_OK))


def correct_delete_resource(identifier: str):
    """
    Mock the request

    :param identifier: identifier of the resource to delete
    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _extract_url(identifier)
    respx.delete(url).mock(return_value=Response(status_code=status.HTTP_200_OK))


# -------------------------------------------------------------------------------------


def error_insert_resource():
    """
    Mock the request

    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _extract_url()
    respx.post(url).mock(return_value=Response(status_code=status.HTTP_404_NOT_FOUND))


def error_update_resource(identifier: str):
    """
    Mock the request

    :param identifier: identifier of the resource to update
    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _extract_url(identifier)
    respx.put(url).mock(return_value=Response(status_code=status.HTTP_404_NOT_FOUND))


def error_delete_resource(identifier: str):
    """
    Mock the request

    :param identifier: identifier of the resource to delete
    """
    correct_get_token(TokenType.client, "Fake_token")
    url = _extract_url(identifier)
    respx.delete(url).mock(return_value=Response(status_code=status.HTTP_404_NOT_FOUND))
