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
from typing import List, Optional

# Third Party
import orjson
from pydantic import Field, validator, constr

# Internal
from .device import Device
from .policy import ServicePolicy, AvailablePolicy
from ..model import OrjsonModel
from ...security.policy_rsa import verify_signature

# -----------------------------------------------------------------------------


def get_service_id(keycloak_response: bytes) -> str:
    """Extract service id from keycloak response"""
    return orjson.loads(keycloak_response)["_id"]


class _Service(OrjsonModel):
    name: constr(to_lower=True) = Field(
        ..., description="service name", example="ServiceA"
    )


class Service(_Service):
    resource_scopes: List[Optional[ServicePolicy]] = Field(
        ...,
        description="policy associated to the service",
        example=[ServicePolicy.storage_policy, ServicePolicy.commercial_policy],
    )


class UserServicesPolicies(AvailablePolicy):
    service_policy_list: List[Optional[Service]] = Field(
        [],
        description="List of services and their associated policies",
        example=[
            {
                "name": "ServiceA",
                "resource_scopes": [
                    ServicePolicy.storage_policy,
                    ServicePolicy.commercial_policy,
                ],
            }
        ],
    )


class GatewayService(OrjsonModel):
    """
    Gateway supported service
    """

    service_list: List[constr(to_lower=True)] = Field(
        ..., description="Services associated to the gateway", example=["ServiceA"]
    )
    sign_device: Device = Field(
        ...,
        title="JWS Device",
        description="Device signed with JWS encryption",
        example="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VfaWQiOiJnaW5vIiwicG9saWN5X2xpc3QiOlsicGlubyJdfQ.hlhRNe6_iufTL1S4WvqzXSDg5RbYC9fm0qseO6zAbs_YZqC_cJC54dJh1r6Nk6HgSp6ku05H3N4yIMDhNvHohljuJzFTXLLKq10gOc2NUpkU85d93pX0mtbZS3XK1TbUDxkh4zJ9hohu-ya00UjXoHuMGYq5QPOxXjM-dwVrxX8",
    )

    @validator("sign_device", pre=True)
    def jws_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError("must be a jws")
        return verify_signature(v)
