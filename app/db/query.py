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
from ..config import get_database_settings

# ---------------------------------------------------------------------------------------


SETTINGS = get_database_settings()
"""Database Settings"""

CREATE_DATABASE = (
    f'CREATE DATABASE "{SETTINGS.postgres_db}" OWNER "{SETTINGS.postgres_user}";'
)
"""Create Database"""

CREATE_TABLE = {
    "service_mapping": """
                    CREATE TABLE IF NOT EXISTS "service_mapping" (
                    keycloak_identifier text,
                    service_id text,
                    username text,
                    policy_list jsonb,
                    PRIMARY KEY(service_id, username)
                    );""",
    "device_mapping": """
                    CREATE TABLE IF NOT EXISTS "device_mapping" (
                    keycloak_identifier text,
                    device_id text,
                    username text,
                    policy_list jsonb,
                    PRIMARY KEY(device_id, username)
                    );""",
}
"""Create database table"""


SELECT = {
    "device": "SELECT policy_list::jsonb FROM device_mapping WHERE device_id = $1;",
    "device_list": "SELECT policy_list::jsonb FROM device_mapping WHERE username = $1 AND keycloak_identifier = $2;",
    "service_keycloak_id": "SELECT keycloak_identifier FROM service_mapping WHERE service_id = $1 AND username = $2;",
    "service_list": "SELECT policy_list::json FROM service_mapping WHERE username = $1;",
    "policy_list": "SELECT policy_list::json FROM service_mapping WHERE service_id = $1;",
}
"Extract data"

DELETE = {
    "device": "DELETE FROM device_mapping WHERE device_id = $1 AND username = $2;",
    "service": "DELETE FROM service_mapping WHERE service_id = $1 AND username = $2;",
}

INSERT = {
    "service": """
        INSERT INTO service_mapping (
        keycloak_identifier,
        service_id,
        username,
        policy_list) VALUES ($1, $2, $3, $4);
    """,
    "device": """
        INSERT INTO device_mapping (
        keycloak_identifier,
        device_id,
        username,
        policy_list) VALUES ($1, $2, $3, $4);
    """,
}
"""Insert data in the database"""

UPDATE = {
    "device": """
        UPDATE device_mapping SET policy_list = $1 WHERE device_id = $2 AND username = $3;
        """,
    "service": """
        UPDATE service_mapping SET policy_list = $1 WHERE service_id = $2 AND username = $3;
        """,
}
