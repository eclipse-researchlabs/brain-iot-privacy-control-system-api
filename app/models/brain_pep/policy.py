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
from enum import Enum
from typing import Optional, List

# Third Party
from pydantic import Field

# Internal
from ..model import OrjsonModel

# -----------------------------------------------------------------------------


class Policy(str, Enum):
    """
    System supported Policy
    """

    anonymization_policy = "anonymization_policy"
    attribution_policy = "attribution_policy"
    commercial_policy = "commercial_policy"
    derivative_data_redistribution_policy = "derivative_data_redistribution_policy"
    disclosure_policy = "disclosure_policy"
    modification_policy = "modification_policy"
    original_data_redistribution_policy = "original_data_redistribution_policy"
    purpose_advertisements_policy = "purpose_advertisements_policy"
    purpose_entertainment_policy = "purpose_entertainment_policy"
    purpose_profiling_policy = "purpose_profiling_policy"
    purpose_public_utility_policy = "purpose_public_utility_policy"
    purpose_recommendation_policy = "purpose_recommendation_policy"
    purpose_safety_policy = "purpose_safety_policy"


class ServicePolicy(str, Enum):
    """
    System supported Policy
    """

    anonymization_policy = "anonymization_policy"
    attribution_policy = "attribution_policy"
    commercial_policy = "commercial_policy"
    derivative_data_redistribution_policy = "derivative_data_redistribution_policy"
    disclosure_policy = "disclosure_policy"
    modification_policy = "modification_policy"
    original_data_redistribution_policy = "original_data_redistribution_policy"
    purpose_advertisements_policy = "purpose_advertisements_policy"
    purpose_entertainment_policy = "purpose_entertainment_policy"
    purpose_profiling_policy = "purpose_profiling_policy"
    purpose_public_utility_policy = "purpose_public_utility_policy"
    purpose_recommendation_policy = "purpose_recommendation_policy"
    purpose_safety_policy = "purpose_safety_policy"
    storage_policy = "storage_policy"


class AvailablePolicy(OrjsonModel):
    available_policy: List[str] = Field(
        ...,
        description="The list of available policies on the system",
        example=[Policy.anonymization_policy, Policy.commercial_policy],
    )
