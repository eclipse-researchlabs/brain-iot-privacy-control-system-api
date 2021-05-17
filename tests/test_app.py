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

# Third Party
from fastapi import status
from fastapi.testclient import TestClient

# Internal
from app.main import app
from app.models.brain_pep.device import Device
from app.models.brain_pep.policy import Policy
from app.models.brain_pep.service import Service, ServicePolicy
from .internals.logger import disable_logger
from .mock.resources import (
    correct_insert_resource,
    correct_delete_resource,
    correct_update_resource,
)
from .mock.policy import correct_get_available_policies
from .mock.attributes import correct_get_user_identifier, correct_set_user_identifier
from .mock.token import correct_get_token, TokenType
from .security.model import RolesEnum
from .security.token import (
    change_default_security_settings,
    generate_fake_token,
    generate_valid_token,
)

# ---------------------------------------------------------------------------------------------


def clear_test():
    """Clear tests"""
    disable_logger()
    change_default_security_settings()


def test_docs_and_startup_shutdown():
    """Test docs and startup and shutdown events"""

    # Load the cache of the documentation
    app.openapi_schema = None
    app.openapi()
    app.openapi()

    with TestClient(app) as client:
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK

    clear_test()


class TestBrainConsumers:
    """
    Test BrainConsumers route
    """

    @respx.mock
    def test_insert_service(self):
        """
        Test insert service
        """
        clear_test()
        correct_insert_resource("test_identifier")
        token = generate_valid_token(
            RolesEnum.brain_consumers, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        fake_service = Service(name="FakeService", resource_scopes=[])
        with TestClient(app) as client:
            for test_token in (token, invalid_token):
                response = client.post(
                    "/api/v1/brain_consumers/service",
                    headers={"Authorization": f"Bearer {test_token}"},
                    json=fake_service.dict(),
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_201_CREATED
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @respx.mock
    def test_get_service(self):
        """
        Test get service
        """
        clear_test()
        correct_get_available_policies(["fake_policy"])
        token = generate_valid_token(
            RolesEnum.brain_consumers, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        with TestClient(app) as client:
            for test_token in (token, invalid_token):
                response = client.get(
                    "/api/v1/brain_consumers/service",
                    headers={"Authorization": f"Bearer {test_token}"},
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_200_OK
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @respx.mock
    def test_delete_service(self):
        """
        Test delete service
        """
        clear_test()
        correct_delete_resource("test_identifier")
        token = generate_valid_token(
            RolesEnum.brain_consumers, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        with TestClient(app) as client:
            for test_token in (token, invalid_token):
                response = client.delete(
                    "/api/v1/brain_consumers/service/fakeservice",
                    headers={"Authorization": f"Bearer {test_token}"},
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_200_OK
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @respx.mock
    def test_update_service(self):
        """
        Test update service
        """
        clear_test()
        correct_insert_resource("test_identifier")
        token = generate_valid_token(
            RolesEnum.brain_consumers, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        fake_service = Service(name="ServiceToUpdate", resource_scopes=[])
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/brain_consumers/service",
                headers={"Authorization": f"Bearer {token}"},
                json=fake_service.dict(),
            )
            assert response.status_code == status.HTTP_201_CREATED

            update_fake_service = Service(
                name="ServiceToUpdate",
                resource_scopes=[ServicePolicy.commercial_policy],
            )
            correct_update_resource("test_identifier")
            for test_token in (token, invalid_token):
                response = client.put(
                    "/api/v1/brain_consumers/service",
                    headers={"Authorization": f"Bearer {test_token}"},
                    json=update_fake_service.dict(),
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_202_ACCEPTED
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestBrainUser:
    """
    Test BrainUser route
    """

    @respx.mock
    def test_insert_device(self):
        """
        Test insert device
        """
        clear_test()
        correct_get_available_policies([])
        correct_get_user_identifier("test_identifier", "fake_id")
       #correct_set_user_identifier("test_identifier")
        token = generate_valid_token(
            RolesEnum.brain_user, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        fake_device = Device(device_id="FakeDevice", policy_list=[])
        with TestClient(app) as client:
            for test_token in (token, invalid_token):
                response = client.post(
                    "/api/v1/brain_user/policy",
                    headers={"Authorization": f"Bearer {test_token}"},
                    json=fake_device.dict(),
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_201_CREATED
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @respx.mock
    def test_get_device_policy(self):
        """
        Test get device policy
        """
        clear_test()
        correct_get_available_policies([Policy.commercial_policy])
        correct_get_user_identifier("test_identifier", "")
        token = generate_valid_token(
            RolesEnum.brain_user, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        with TestClient(app) as client:
            for test_token in (token, invalid_token):
                response = client.get(
                    "/api/v1/brain_user/policy",
                    headers={"Authorization": f"Bearer {test_token}"},
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_200_OK
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @respx.mock
    def test_update_device(self):
        """
        Test update device
        """
        clear_test()
        token = generate_valid_token(
            RolesEnum.brain_user, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        fake_device = Device(
            device_id="FakeDevice", policy_list=[Policy.commercial_policy]
        )
        with TestClient(app) as client:
            for test_token in (token, invalid_token):
                response = client.put(
                    "/api/v1/brain_user/policy",
                    headers={"Authorization": f"Bearer {test_token}"},
                    json=fake_device.dict(),
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_202_ACCEPTED
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @respx.mock
    def test_delete(self):
        """
        Test delete device
        """
        clear_test()
        token = generate_valid_token(
            RolesEnum.brain_user, "test_user", "test_identifier"
        )
        invalid_token = generate_fake_token()
        with TestClient(app) as client:
            for test_token in (token, invalid_token):
                response = client.delete(
                    "/api/v1/brain_user/policy/FakeDevice",
                    headers={"Authorization": f"Bearer {test_token}"},
                )
                if test_token == token:
                    assert response.status_code == status.HTTP_200_OK
                else:
                    assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGateway:
    """
    Test Gateway route
    """

    @respx.mock
    def test_get_device(self):
        """
        Test get device
        """
        clear_test()
        correct_get_available_policies([])
        correct_get_user_identifier("test_identifier", "fake")
        token = generate_valid_token(
            RolesEnum.brain_user, "test_user", "test_identifier"
        )
        fake_device = Device(device_id="FakeDevice", policy_list=[])
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/brain_user/policy",
                headers={"Authorization": f"Bearer {token}"},
                json=fake_device.dict(),
            )

            assert response.status_code == status.HTTP_201_CREATED

            response = client.get("/api/v1/gateway/device/device_not_found")
            assert response.status_code == status.HTTP_404_NOT_FOUND
            response = client.get("/api/v1/gateway/device/FakeDevice")
            assert response.status_code == status.HTTP_200_OK

    @respx.mock
    def test_filter(self):
        """
        Test filter
        """
        clear_test()
        correct_insert_resource("test_identifier")
        token = generate_valid_token(
            RolesEnum.brain_consumers, "test_user", "test_identifier"
        )
        fake_service = Service(name="FakeService", resource_scopes=[])
        gateway = {"service_list": ["fakeservice"], "sign_device": ""}
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/brain_consumers/service",
                headers={"Authorization": f"Bearer {token}"},
                json=fake_service.dict(),
            )
            assert response.status_code == status.HTTP_201_CREATED

            response = client.get("/api/v1/gateway/device/FakeDevice")
            assert response.status_code == status.HTTP_200_OK
            gateway["sign_device"] = response.json()["signature"]
            response = client.post("/api/v1/gateway/filter", json=gateway)
            assert response.status_code == status.HTTP_200_OK
