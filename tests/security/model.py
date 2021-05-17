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
from datetime import datetime, timedelta
from typing import List

# Third PArty
from fastuuid import uuid4
from pydantic import Field

# Internal
from app.models.model import OrjsonModel
from .constants import ISSUER, AUDIENCE

# ----------------------------------------------------------------------------------


class RolesEnum(str, Enum):
    brain_consumers = "brain_consumers"
    brain_user = "brain_user"
    fake = "FakeToken"


class Roles(OrjsonModel):
    roles: List[RolesEnum]


class Token(OrjsonModel):
    jti: str = str(uuid4())
    exp: datetime = datetime.utcnow() + timedelta(seconds=300)
    nbf: int = 0
    iat: datetime = datetime.utcnow() + timedelta(seconds=0.5)
    iss: str = ISSUER
    aud: str = AUDIENCE
    sub: str = str(uuid4())
    typ: str = "Bearer"
    azp: str = "client_pub"
    auth_time: int = 0
    session_state: str = str(uuid4())
    acr: int = 1
    client_session: str = str(uuid4())
    allowed_origins: list = []
    realm_access: Roles
    resource_access: dict = {"roles": ["Testing"]}
    name: str = ""
    preferred_username: str
