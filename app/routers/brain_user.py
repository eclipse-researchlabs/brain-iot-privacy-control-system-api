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
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import ORJSONResponse

# Internal
from ..internals.policy.device import (
    insert_user_device_policies,
    delete_user_device_policies,
    update_user_device_policies,
    get_user_device_policies,
)

from ..models.brain_pep.device import Device, UserDevicesPolicy
from ..models.response import PolicyUpdated
from ..models.security import Requester
from ..security.jwt_bearer import Signature


# --------------------------------------------------------------------------------------------


# JWT Signature
user_auth = Signature(realm_access="brain_user", return_requester=True)
router = APIRouter(prefix="/api/v1/brain_user", tags=["BrainUser"])


@router.get(
    "/policy",
    response_class=ORJSONResponse,
    response_model=UserDevicesPolicy,
    response_model_exclude_none=True,
    summary="Extract BrainUsers devices policies",
)
async def get_policies(
    requester: Requester = Depends(user_auth),
):
    """
    This endpoint provides a way to get a list of the available policies and the ones already set on the
     user's devices. Available policies are all the ones set on the brain-iot domain to be associated to a specific
     device by the user.
    """

    return await get_user_device_policies(requester)


@router.post(
    "/policy",
    response_model=PolicyUpdated,
    response_class=ORJSONResponse,
    summary="Set BrainUsers devices policies",
    status_code=status.HTTP_201_CREATED,
)
async def insert_user_policies(
    client: Requester = Depends(user_auth),
    device: Device = Body(...),
):
    """
    This endpoint provides a way to set the selected policies on the user's devices as attribute of the user.
    The user will inherit the union of the policies of his devices.
    """
    # Set device policies
    return await insert_user_device_policies(client, device)


@router.put(
    "/policy",
    response_model=PolicyUpdated,
    response_class=ORJSONResponse,
    summary="Update BrainUsers devices policies",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user_policies(
    client: Requester = Depends(user_auth),
    device: Device = Body(...),
):
    """
    This endpoint provides a way to update the selected policies on the user's devices as attribute of the user.
    The user will inherit the union of the policies of his devices.
    """

    # Update device policies
    return await update_user_device_policies(client, device)


@router.delete(
    "/policy/{device_id}",
    response_model=PolicyUpdated,
    response_class=ORJSONResponse,
    summary="Delete BrainUsers devices policies",
    status_code=status.HTTP_200_OK,
)
async def delete_user_policies(device_id: str, client: Requester = Depends(user_auth)):
    """
    This endpoint provides a way to delete the selected policies on the user's devices as attribute of the user.
    The user will inherit the union of the policies of his devices.
    """

    # delete device policies
    return await delete_user_device_policies(client, device_id)
