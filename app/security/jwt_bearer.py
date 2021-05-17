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
from typing import List, Optional, Union

# Third Party
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from jose import jwt, JWTError

# Internal
from ..config import get_security_settings
from ..internals.logger import get_logger
from ..models.security import Requester


# ----------------------------------------------------------------------------------------


class Signature(HTTPBearer):
    def __init__(
        self,
        realm_access: str,
        return_requester: bool = False,
    ):
        super().__init__()
        self.realm_access = realm_access
        self.return_requester = return_requester

    async def __call__(self, request: Request) -> Optional[Union[List[str], Requester]]:
        # extract credentials
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        jwt_token = credentials.credentials

        # Get Security settings
        settings = get_security_settings()
        try:
            token = jwt.decode(
                jwt_token,
                f"-----BEGIN PUBLIC KEY-----\n"
                f"{settings.realm_public_key}"
                f"\n-----END PUBLIC KEY-----"
                "",
                settings.algorithm,
                issuer=settings.issuer,
                options={
                    "verify_aud": False,
                },
            )
        except JWTError as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_bearer_token"
            )

        # Get Logger
        logger = get_logger()

        if self.realm_access not in token["realm_access"]["roles"]:
            # Token debug
            await logger.debug({"token_roles": token["realm_access"]["roles"]})
            # Raise exception
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_bearer_token"
            )

        if self.return_requester:
            try:
                return Requester.parse_obj(token)
            except ValidationError:
                # Token debug
                await logger.debug({"msg": "Invalid keycloak settings", "token": token})
                # Raise exception
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="invalid keycloak settings",
                )
