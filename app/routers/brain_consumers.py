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
from ..internals.policy.service import (
    get_service,
    insert_service,
    update_service,
    delete_service,
)
from ..models.brain_pep.service import Service, UserServicesPolicies
from ..models.response import ServiceUpdated
from ..models.security import Requester
from ..security.jwt_bearer import Signature


# --------------------------------------------------------------------------------------------


# JWT Signature
user_auth = Signature(realm_access="brain_consumers", return_requester=True)
router = APIRouter(prefix="/api/v1/brain_consumers", tags=["BrainConsumers"])


@router.get(
    "/service",
    response_class=ORJSONResponse,
    response_model=UserServicesPolicies,
    summary="Extract policies foreseen by a service",
)
async def get_foreseen_policies(
    requester: Requester = Depends(user_auth),
):
    """
    This endpoint provides a way to get a list of the available policies and the ones already set on the
     user's devices. Available policies are all the ones set on the brain-iot domain to be associated to a specific
     device by the user.
    """

    # Get BrainPep token
    return await get_service(requester)


@router.post(
    "/service",
    response_model=ServiceUpdated,
    response_class=ORJSONResponse,
    summary="Set policies foreseen by a service",
    status_code=status.HTTP_201_CREATED,
)
async def insert_foreseen_policies(
    requester: Requester = Depends(user_auth), service: Service = Body(...)
):
    """
    This endpoint provides a way to set the selected policies on the user's devices as attribute of the user.
    The user will inherit the union of the policies of his devices.
    """

    # Set policies
    return await insert_service(service, requester)


@router.put(
    "/service",
    response_model=ServiceUpdated,
    response_class=ORJSONResponse,
    summary="Update policies foreseen by a service",
    dependencies=[Depends(user_auth)],
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_foreseen_policies(
    requester: Requester = Depends(user_auth), service: Service = Body(...)
):
    """
    This endpoint provides a way to update the selected policies on the user's devices as attribute of the user.
    The user will inherit the union of the policies of his devices.
    """
    return await update_service(service, requester)


@router.delete(
    "/service/{service_id}",
    response_model=ServiceUpdated,
    response_class=ORJSONResponse,
    summary="Delete policies foreseen by a service",
    status_code=status.HTTP_200_OK,
)
async def delete_foreseen_policies(
    service_id: str, requester: Requester = Depends(user_auth)
):
    """
    This endpoint provides a way to delete the selected policies on the user's devices as attribute of the user.
    The user will inherit the union of the policies of his devices.
    """
    return await delete_service(service_id, requester)
