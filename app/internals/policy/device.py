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
from ..keycloak.attributes import get_user_identifier, set_user_identifier
from ..keycloak.token import get_admin_token
from ..keycloak.policy import get_available_policies
from ...db.postgresql import get_database
from ...models.brain_pep.device import Device, UserDevicesPolicy
from ...models.response import PolicyUpdated
from ...models.security import Requester, SignedMessage
from ...security.policy_rsa import sign_user_policies

# ---------------------------------------------------------------------------------------


async def insert_user_device_policies(
    client: Requester,
    device: Device,
) -> PolicyUpdated:
    """
    Set User's devices policies

    :param client: Requester
    :param device: Device and it's associated policies
    """

    # Obtain an admin token
    admin_token = await get_admin_token()
    # Extract user identifier fro keycloak
    identifier = await get_user_identifier(admin_token, client.sub)
    if identifier is None:
        # Generate a new one and store it in keycloak
        identifier = await set_user_identifier(admin_token, client.sub)

    # Get database
    database = get_database()
    await database.insert_device(identifier, device, client.preferred_username)
    return PolicyUpdated()


# ---------------------------------------------------------------------------------------


async def update_user_device_policies(
    client: Requester,
    device: Device,
) -> PolicyUpdated:
    """
    Update User's devices policies

    :param client: Requester
    :param device: Device and it's associated policies
    """
    # Get database
    database = get_database()
    await database.update_device(device, client.preferred_username)
    return PolicyUpdated()


# ---------------------------------------------------------------------------------------


async def delete_user_device_policies(
    client: Requester,
    device_id: str,
) -> PolicyUpdated:
    """
    Update User's devices policies

    :param client: Requester
    :param device_id: Device identifier
    """
    # Get database
    database = get_database()
    await database.delete_device(device_id, client.preferred_username)
    return PolicyUpdated()


# ---------------------------------------------------------------------------------------


async def get_user_device_policies(
    client: Requester,
) -> UserDevicesPolicy:
    """
    Set User's devices policies

    :param client: Requester
    """

    # Obtain an admin token
    admin_token = await get_admin_token()
    # Extract available_policy
    available_policy = await get_available_policies(admin_token)
    # Extract user identifier from keycloak
    identifier = await get_user_identifier(admin_token, client.sub)
    if identifier is None:
        return UserDevicesPolicy(available_policy=available_policy)

    # Get database
    database = get_database()
    device_list = await database.extract_all_devices(
        identifier, client.preferred_username
    )
    return UserDevicesPolicy(
        available_policy=available_policy, device_policy_list=device_list
    )


# ---------------------------------------------------------------------------------------


async def get_device_policies(device_id: str) -> SignedMessage:
    """
    Extract a Policies from BrainPep-API

    :param device_id: Device identifier
    :return: DevicePolicyMapStrSigned
    """
    database = get_database()
    device = await database.extract_device(device_id)
    return SignedMessage(signature=sign_user_policies(device.signature_conversion()))
