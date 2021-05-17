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

# Internal
from .model import OrjsonModel

# Third Party
from pydantic import Field

# ---------------------------------------------------------------


class Requester(OrjsonModel):
    """
    Requester Model

    preferred_username: User name
    sub: User identifier
    """

    preferred_username: str
    """User name"""

    sub: str
    """User identifier"""


# ---------------------------------------------------------------


class Role(OrjsonModel):
    """Requester Model"""

    role: str
    user: Optional[str]


# ---------------------------------------------------------------


class Token(OrjsonModel):
    """Token obtained from Keycloak"""

    access_token: str


class SignedMessage(OrjsonModel):
    """Signed message model"""

    signature: str = Field(
        ...,
        description="Signed device information",
        example="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VfaWQiOiJkZXZpY2VfYSIsInBvbGljeV9saXN0IjpbImNvbW1lcmNpYWxfcG9saWN5IiwiYW5vbnltaXphdGlvbl9wb2xpY3kiXSwic3RvcmFnZV9wb2xpY3kiOm51bGx9.L5PzTmHkAIhuMNbWuXvyNyICYEiIFFuG6FO7HM0WDTiOZPZAP_OgYf-rXRiDU8d5EzcbwO1p6Wg9xiy9Q5-vzOiaZVPE74KjyEOGe1ARjoYYqMkl13ZuU4SWtbWpsj9y9Wu8ofcU4h3lmdRXm6Y1Aw6hqUzo5oYhTEACszcVbKo",
    )
