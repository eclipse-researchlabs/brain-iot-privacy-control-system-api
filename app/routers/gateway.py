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
from fastapi import APIRouter, Body, Path
from fastapi.responses import ORJSONResponse

# Internal
from ..db.postgresql import get_database
from ..internals.policy.device import get_device_policies

from ..models.brain_pep.service import GatewayService, Service
from ..models.security import SignedMessage

# --------------------------------------------------------------------------------------------

router = APIRouter(prefix="/api/v1/gateway", tags=["Gateway"])


@router.post(
    "/filter",
    response_class=ORJSONResponse,
    response_model=List[Service],
    response_model_exclude_none=True,
    summary="Get filtered list of allowed services",
)
async def filter_service_list(
    gateway_service: GatewayService = Body(...),
):
    """
    This endpoint provides a way to filter a list of services based on a list of policies signed
    by the brain-pep.
    This API will receive both a list of service_ids and a token containing the list of signed policies
    associated with the incoming message to be forwarded to the services.
    """
    database = get_database()
    return await database.filter_service_list(gateway_service)


@router.get(
    "/device/{device_id}",
    response_class=ORJSONResponse,
    response_model=SignedMessage,
    summary="Get policies of a device",
)
async def get_device_policy_mapping(
    device_id: str = Path(
        ...,
        description="The device id to look for the policies",
        example="device_a",
        max_length=30,
    )
):
    """
    This endpoint provides a way to get the list of roles/policies (signed) by providing device_id (MAC)
    Should be used by the component that wants to know the policies to be associated to
    the message before forwarding it.
    """
    return await get_device_policies(device_id)
