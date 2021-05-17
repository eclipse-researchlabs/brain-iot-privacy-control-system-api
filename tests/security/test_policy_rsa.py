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
import pytest

# Third Party
from fastapi.exceptions import HTTPException

# Internal
from app.models.brain_pep.device import Device, Policy
from app.security.policy_rsa import sign_user_policies, verify_signature
from .token import change_default_security_settings

# ------------------------------------------------------------------------------


class TestJWS:
    """
    Test the generation of jws
    """

    def test_signature(self):
        """
        Test the signature
        """
        change_default_security_settings()
        fake_device = Device(device_id="fake", policy_list=[Policy.disclosure_policy])
        signed_device = sign_user_policies(fake_device.signature_conversion())
        verified_device = verify_signature(signed_device)
        verified_device = Device.parse_obj(verified_device)
        assert verified_device == fake_device, "Must be equal"

        with pytest.raises(HTTPException):
            verify_signature("Fake signature")
