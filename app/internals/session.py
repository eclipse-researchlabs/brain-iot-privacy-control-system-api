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

# Standard library
from functools import lru_cache

# Third Party
from httpx import AsyncClient

# ----------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def get_keycloak_session() -> AsyncClient:
    """
    Instantiate a session
    """
    return AsyncClient(verify=False)


async def close_keycloak_session():
    """
    Close the instantiated session
    """
    session = get_keycloak_session()
    await session.aclose()
    get_keycloak_session.cache_clear()
