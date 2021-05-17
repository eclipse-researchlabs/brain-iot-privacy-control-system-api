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
from datetime import datetime, timedelta

# Third Party
from jose import jwt

# Internal
from app.config import get_security_settings
from .constants import PRIVATE_KEY, ISSUER, PUBLIC_KEY, AUDIENCE
from .model import Token, Roles, RolesEnum

# ------------------------------------------------------------------------------------------


def change_default_security_settings():
    """Change the default security settings for testing purpose"""
    settings = get_security_settings()
    settings.issuer = ISSUER
    settings.realm_public_key = PUBLIC_KEY
    settings.audience = AUDIENCE
    settings.jws_public_key = PUBLIC_KEY
    settings.jws_private_key = PRIVATE_KEY


def generate_fake_token() -> str:
    """
    Generate a fake token to ensure that the app is secure

    :return: token
    """
    to_encode = Token(
        exp=datetime.utcnow() - timedelta(seconds=300),
        iat=datetime.utcnow() - timedelta(seconds=301),
        realm_access=Roles(roles=[RolesEnum.fake]),
        preferred_username="Fake",
    ).dict()

    return jwt.encode(
        to_encode,
        f"-----BEGIN RSA PRIVATE KEY-----\n"
        f"{PRIVATE_KEY}"
        f"\n-----END RSA PRIVATE KEY-----",
        algorithm="RS256",
    )


def generate_valid_token(realm: str, username: str, sub: str) -> str:
    """
    Generate a valid token

    :param realm: realm access role
    :param username: client
    :param sub: identifier
    :return: token
    """
    to_encode = Token(
        exp=datetime.utcnow() + timedelta(seconds=300),
        iat=datetime.utcnow(),
        realm_access=Roles(roles=[RolesEnum(realm)]),
        sub=sub,
        preferred_username=username,
    ).dict()

    return jwt.encode(
        to_encode,
        f"-----BEGIN RSA PRIVATE KEY-----\n"
        f"{PRIVATE_KEY}"
        f"\n-----END RSA PRIVATE KEY-----",
        algorithm="RS256",
    )
