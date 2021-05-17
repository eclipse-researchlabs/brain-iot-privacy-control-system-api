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

# Internal
from ...config import get_keycloak_admin_settings, get_brainpep_settings

# ----------------------------------------------------------------------------------

_ADMIN_SETTINGS = get_keycloak_admin_settings()
"""Administrator Settings"""
_CLIENT_SETTINGS = get_brainpep_settings()
"""BrainPeP Settings"""


ADMIN_DATA = {
    "url": _ADMIN_SETTINGS.admin_token_request_url,
    "data": {
        "client_id": _ADMIN_SETTINGS.admin_client_id,
        "username": _ADMIN_SETTINGS.admin_username,
        "password": _ADMIN_SETTINGS.admin_password,
        "grant_type": _ADMIN_SETTINGS.admin_grant_type,
    },
}
"""Administrator Data"""


CLIENT_DATA = {
    "url": _CLIENT_SETTINGS.client_token_request_url,
    "data": {
        "client_id": _CLIENT_SETTINGS.client_id,
        "client_secret": _CLIENT_SETTINGS.client_secret,
        "grant_type": _CLIENT_SETTINGS.client_grant_type,
    },
}
"""Client Data"""
