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

# Test
import respx
import pytest
import uvloop
from fastapi import HTTPException

# Internal
from app.internals.keycloak.attributes import get_user_identifier, set_user_identifier
from app.internals.keycloak.policy import get_available_policies
from app.internals.keycloak.resources import (
    insert_resource,
    update_resource,
    delete_resource,
)
from app.internals.keycloak.token import get_brain_pep_token, get_admin_token
from app.internals.session import close_keycloak_session
from app.models.brain_pep.service import Service

# Mock
from ..mock.attributes import (
    correct_get_user_identifier,
    correct_set_user_identifier,
    error_get_user_identifier,
    error_set_user_identifier,
)
from ..mock.policy import correct_get_available_policies
from ..mock.resources import (
    correct_insert_resource,
    correct_update_resource,
    correct_delete_resource,
    error_insert_resource,
    error_update_resource,
    error_delete_resource,
)

from ..mock.token import correct_get_token, TokenType, error_get_token

# ------------------------------------------------------------------------------


@pytest.fixture()
def event_loop():
    """
    Set uvloop as the default event loop
    """
    loop = uvloop.Loop()
    yield loop
    loop.close()


class TestGetKeycloakToken:
    """
    Test the extraction of a token from keycloak
    """

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_client_token(self):
        """Test the behaviour of get_brain_pep_token"""

        # Mock the request
        correct_get_token(TokenType.client, "ClientToken")
        token = await get_brain_pep_token()
        assert token == "ClientToken", "Token must be equal"
        with pytest.raises(HTTPException):
            error_get_token(TokenType.client)
            await get_brain_pep_token()
        await close_keycloak_session()

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_admin_token(self):
        """Test the behaviour of get_brain_pep_token"""

        # Mock the request
        correct_get_token(TokenType.admin, "AdminToken")
        token = await get_admin_token()
        assert token == "AdminToken", "Token must be equal"
        with pytest.raises(HTTPException):
            error_get_token(TokenType.admin)
            await get_admin_token()
        await close_keycloak_session()


class TestKeycloakAttributes:
    """
    Test the extraction and setting of attributes on keycloak
    """

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_user_identifier(self):
        """Test the behaviour of get_user_identifier"""

        # Mock the request
        correct_get_user_identifier("keycloak_id", "requested_id")
        requested_id = await get_user_identifier("fake_token", "keycloak_id")
        assert requested_id == "requested_id", "Requested id must be equal"
        with pytest.raises(HTTPException):
            error_get_user_identifier("keycloak_id")
            requested_id = await get_user_identifier("fake_token", "keycloak_id")
        await close_keycloak_session()

    @respx.mock
    @pytest.mark.asyncio
    async def test_set_user_identifier(self):
        """Test the behaviour of set_user_identifier"""

        # Mock the request
        correct_set_user_identifier("keycloak_id")
        await set_user_identifier("fake_token", "keycloak_id")
        with pytest.raises(HTTPException):
            error_set_user_identifier("keycloak_id")
            await set_user_identifier("fake_token", "keycloak_id")
        await close_keycloak_session()


class TestKeycloakPolicies:
    """
    Test the extraction of the policies stored in keycloak
    """

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_available_policies(self):
        """Test the behaviour of get_available_policies"""

        # Mock the request
        correct_get_available_policies(["policy_1"])
        policy_list = await get_available_policies()
        assert policy_list == ["policy_1"], "Policy must be equal"
        await close_keycloak_session()


class TestKeycloakResources:
    """
    Test the extraction and setting of resources on keycloak
    """

    @respx.mock
    @pytest.mark.asyncio
    async def test_insert_resource(self):
        """Test the behaviour of get_user_identifier"""
        resource = Service(name="Fake_service", resource_scopes=[])
        # Mock the request
        correct_insert_resource("fake_identifier")
        resource_identifier = await insert_resource(resource)
        assert resource_identifier == "fake_identifier", "Identifier must be equal"
        with pytest.raises(HTTPException):
            error_insert_resource()
            await insert_resource(resource)
        await close_keycloak_session()

    @respx.mock
    @pytest.mark.asyncio
    async def test_update_resource(self):
        """Test the behaviour of get_user_identifier"""
        resource = Service(name="Fake_service", resource_scopes=[])
        # Mock the request
        correct_update_resource("fake_identifier")
        await update_resource("fake_identifier", resource)
        with pytest.raises(HTTPException):
            error_update_resource("fake_identifier")
            await update_resource("fake_identifier", resource)
        await close_keycloak_session()

    @respx.mock
    @pytest.mark.asyncio
    async def test_delete_resource(self):
        """Test the behaviour of get_user_identifier"""
        # Mock the request
        correct_delete_resource("fake_identifier")
        await delete_resource("fake_identifier")
        with pytest.raises(HTTPException):
            error_delete_resource("fake_identifier")
            await delete_resource("fake_identifier")
        await close_keycloak_session()
