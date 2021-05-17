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
from datetime import datetime
from typing import List, Optional

# Third Party
from pydantic import Field, validator
from orjson import dumps

# Internal
from .policy import Policy, AvailablePolicy
from ..model import OrjsonModel

# -----------------------------------------------------------------------------


class _Device(OrjsonModel):
    device_id: str = Field(..., description="Device identifier", example="4eeb")


class Device(_Device):
    """Device model"""

    policy_list: List[Optional[Policy]] = Field(
        ...,
        description="List of policy associated to the device",
        example=[
            Policy.anonymization_policy,
            Policy.attribution_policy,
            Policy.commercial_policy,
            Policy.derivative_data_redistribution_policy,
            Policy.disclosure_policy,
            Policy.modification_policy,
            Policy.original_data_redistribution_policy,
            Policy.purpose_advertisements_policy,
            Policy.purpose_entertainment_policy,
            Policy.purpose_profiling_policy,
            Policy.purpose_public_utility_policy,
            Policy.purpose_recommendation_policy,
            Policy.purpose_safety_policy,
        ],
    )
    storage_policy: Optional[datetime] = Field(
        default=None,
        description="specifies whether and how long the Data of Data Owner is allowed be stored.",
        example="2021-05-07T07:50:39.818706+00:00",
    )

    @validator("storage_policy")
    def policy_storage_must_be_without_timezones(cls, v):
        if v:
            return v.replace(tzinfo=None)

    def signature_conversion(self) -> bytes:
        """
        Convert model to be used with python-jose

        :return: model in bytes format
        """
        return dumps(self.dict(exclude_none=True))


class SignedDevice(Device):
    signature: str = Field(
        ...,
        description="The JWS token containing the list of policies signed by the authorization service",
        examples="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VfaWQiOiJkZXZpY2VfYSIsInBvbGljeV9saXN0IjpbImNvbW1lcmNpYWxfcG9saWN5IiwiYW5vbnltaXphdGlvbl9wb2xpY3kiXSwic3RvcmFnZV9wb2xpY3kiOm51bGx9.L5PzTmHkAIhuMNbWuXvyNyICYEiIFFuG6FO7HM0WDTiOZPZAP_OgYf-rXRiDU8d5EzcbwO1p6Wg9xiy9Q5-vzOiaZVPE74KjyEOGe1ARjoYYqMkl13ZuU4SWtbWpsj9y9Wu8ofcU4h3lmdRXm6Y1Aw6hqUzo5oYhTEACszcVbKo",
    )


class UserDevicesPolicy(AvailablePolicy):
    """User device Policy made by me"""

    device_policy_list: List[Optional[Device]] = Field(
        [],
        description="List of devices and their associated policies",
        example=[
            {
                "device_id": "4eeb",
                "policy_list": [
                    Policy.anonymization_policy,
                    Policy.attribution_policy,
                    Policy.commercial_policy,
                    Policy.derivative_data_redistribution_policy,
                ],
            }
        ],
    )
