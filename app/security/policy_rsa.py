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
from functools import lru_cache
from typing import Union

# Third Party
from fastapi import HTTPException, status
from jose import jws, JWSError
from orjson import loads

# Internal
from ..config import get_security_settings

# ----------------------------------------------------------------------------------------


@lru_cache(maxsize=32)
def sign_user_policies(policies: Union[bytes, dict]) -> str:
    """
    Sign user policies

    :param policies: data to sign
    :return: data signed in a string format
    """
    settings = get_security_settings()
    return jws.sign(
        policies,
        f"-----BEGIN RSA PRIVATE KEY-----\n"
        f"{settings.jws_private_key}"
        f"\n-----END RSA PRIVATE KEY-----"
        "",
        algorithm=settings.jws_algorithm,
    )


@lru_cache(maxsize=32)
def verify_signature(sig: str) -> dict:
    """
    Verify signed message

    :param sig: signature
    :return: user policies
    """
    settings = get_security_settings()
    try:
        return loads(
            jws.verify(
                sig,
                f"-----BEGIN PUBLIC KEY-----\n"
                f"{settings.jws_public_key}"
                f"\n-----END PUBLIC KEY-----"
                "",
                algorithms=settings.jws_algorithm,
            )
        )
    except JWSError:
        # In python lru_cache won't cache exceptions
        # so an HTTPException will always be  raised in case of invalid signature
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid jws"
        )
