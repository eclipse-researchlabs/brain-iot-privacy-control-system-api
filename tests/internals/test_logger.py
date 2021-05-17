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
import uvloop

# Third Party
from asyncpg.exceptions import PostgresError

# Internal
from app.internals.logger import log_postgres_error

# ------------------------------------------------------------------------------


@pytest.fixture()
def event_loop():
    """
    Set uvloop as the default event loop
    """
    loop = uvloop.Loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_logger():
    error = PostgresError("FakeError")
    await log_postgres_error(error)
