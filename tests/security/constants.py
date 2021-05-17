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
import os

# -------------------------------------------------------------------------------------------------------------
PATH = os.path.abspath(os.path.dirname(__file__))
"""Path to the directory containing private.pem and public.pem"""

ISSUER = "Travis-ci/test"
"""Used only for CI"""

AUDIENCE = "Travis-ci/test"
"""Used only for CI"""

with open(f"{PATH}/public.pem", "r") as fp:
    PUBLIC_KEY = fp.read()
"""Public token key used for testing purpose"""

with open(f"{PATH}/private.pem", "r") as fp:
    PRIVATE_KEY = fp.read()
"""Private token key used for testing purpose"""
