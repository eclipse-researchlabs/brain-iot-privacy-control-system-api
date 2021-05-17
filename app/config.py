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

# Third Party
from pydantic import BaseSettings

# --------------------------------------------------------------


class AdminKeycloak(BaseSettings):
    admin_client_id: str
    admin_client_secret: str
    admin_grant_type: str
    admin_password: str
    admin_token_request_url: str
    admin_username: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_keycloak_admin_settings() -> AdminKeycloak:
    return AdminKeycloak()


class BrainPEPSettings(BaseSettings):
    client_id: str
    client_secret: str
    client_grant_type: str
    client_password: str
    client_token_request_url: str
    resource_request_url: str
    policy_request_url: str
    user_attribute_request_url: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_brainpep_settings() -> BrainPEPSettings:
    return BrainPEPSettings()


# --------------------------------------------------------------


class DatabaseSettings(BaseSettings):
    connection_number: int
    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_pwd: str
    postgres_user: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


# --------------------------------------------------------------


class SecuritySettings(BaseSettings):
    algorithm: str
    audience: str
    issuer: str
    jws_private_key: str
    jws_public_key: str
    jws_algorithm: str
    realm_public_key: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_security_settings() -> SecuritySettings:
    return SecuritySettings()


# --------------------------------------------------------------
