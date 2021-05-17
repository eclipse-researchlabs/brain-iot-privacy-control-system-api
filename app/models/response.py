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

# Third Party
from pydantic import Field

# Internal
from .model import OrjsonModel

# --------------------------------------------------------------------------------------------


class Updated(OrjsonModel):
    resource: str
    updated: bool = Field(True, example=True)


class PolicyUpdated(Updated):
    resource: str = Field("policy", example="policy")


class ServiceUpdated(Updated):
    resource: str = Field("service", example="service")
