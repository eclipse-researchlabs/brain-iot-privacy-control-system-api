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
from typing import List

# Third Party
from pydantic import validator

# Internal
from ..model import OrjsonModel

# -----------------------------------------------------------------------------


class DevicePolicyList(OrjsonModel):
    device_policy_list: str

    @validator("device_policy_list", pre=True)
    def extract_only_first_element(cls, v: List[str]):
        """
        Extract only first argument from the list of attributes on keycloak

        :param v: data to validate
        :return: unique identifier of device policy list
        """
        return list(v)[0]


class Attributes(OrjsonModel):
    """
    Model used to extract device_policy_list from keycloak
    """

    attributes: DevicePolicyList
