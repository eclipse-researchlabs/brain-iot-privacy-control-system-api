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

# Internal
from ..keycloak.policy import get_available_policies
from ..keycloak.resources import delete_resource, update_resource, insert_resource
from ...db.postgresql import get_database
from ...models.response import ServiceUpdated
from ...models.security import Requester
from ...models.brain_pep.service import (
    Service,
    UserServicesPolicies,
)

# ---------------------------------------------------------------------------------------


async def get_service(
    service_requested: Requester,
) -> UserServicesPolicies:
    """
    Extract service from keycloak

    :param service_requested: Service of interest
    :return: Requested Service if found
    """

    # Get database
    database = get_database()

    # Extract available policy
    available_policy = await get_available_policies()

    # extract service list
    service_list = await database.extract_all_services(
        service_requested.preferred_username
    )
    return UserServicesPolicies(
        available_policy=available_policy, service_policy_list=service_list
    )


async def insert_service(service: Service, requester: Requester) -> ServiceUpdated:
    """
    Set Service policies

    :param service: Service to store
    :param requester: Client
    """
    # Store resource in keycloak
    identifier = await insert_resource(service)

    # Store in the database
    database = get_database()
    await database.insert_service(identifier, requester.preferred_username, service)
    return ServiceUpdated()


async def update_service(service: Service, requester: Requester) -> ServiceUpdated:
    """
    Set Service policies

    :param service: Service to store
    :param requester: Client
    """

    # Get Database
    database = get_database()
    identifier = await database.extract_service_keycloak_identifier(
        service.name, requester.preferred_username
    )

    # Update resource on keycloak
    await update_resource(identifier, service)

    # Update database
    await database.update_service(service, requester.preferred_username)
    return ServiceUpdated()


async def delete_service(service_id: str, client: Requester) -> ServiceUpdated:
    """
    Update User's devices policies

    :param service_id: Service identifier
    :param client: Requester
    """
    # Get database
    database = get_database()
    identifier = await database.extract_service_keycloak_identifier(
        service_id, client.preferred_username
    )
    if identifier:
        # Delete service from keycloak
        await delete_resource(identifier)
        # Delete from the database
        await database.delete_service(service_id, client.preferred_username)
    return ServiceUpdated()
