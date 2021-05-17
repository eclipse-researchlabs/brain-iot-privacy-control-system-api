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
from typing import List

# Third Party
from fastapi import status
from httpx import Response
import respx

# Internal
from app.config import get_brainpep_settings
from .token import correct_get_token, TokenType

# ----------------------------------------------------------------------------------


def correct_get_available_policies(policy_list_to_return: List[str]):
    """
    Mock keycloak http request

    :param policy_list_to_return: policy to return
    """
    correct_get_token(TokenType.admin, "fake_token")
    # Get settings
    settings = get_brainpep_settings()
    respx.get(settings.policy_request_url).mock(
        return_value=Response(
            status_code=status.HTTP_200_OK,
            json=[{"name": policy} for policy in policy_list_to_return],
        )
    )
