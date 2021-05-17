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


# Standard library
from functools import lru_cache
import time
from typing import List, Optional

# Third party
from asyncpg import connect, create_pool, Connection
from asyncpg.exceptions import (
    PostgresError,
    InvalidCatalogNameError,
    DuplicateDatabaseError,
)
from asyncpg.pool import Pool
from fastapi import status, HTTPException

# Internal
from .query import (
    CREATE_DATABASE,
    CREATE_TABLE,
    DELETE,
    INSERT,
    SELECT,
    SETTINGS,
    UPDATE,
)

from ..internals.logger import log_postgres_error
from app.models.brain_pep.device import Device
from app.models.brain_pep.service import Service, GatewayService

# ---------------------------------------------------------------------------------------


class DataBase:
    pool: Pool = None
    """Connection pool to the database"""

    @staticmethod
    async def __create_table_service_mapping(sys_conn: Connection):
        await sys_conn.execute(CREATE_TABLE["service_mapping"])

    @staticmethod
    async def __create_table_device_mapping(sys_conn: Connection):
        await sys_conn.execute(CREATE_TABLE["device_mapping"])

    @classmethod
    async def connect(cls) -> None:
        """
        Create a connection pool to the database
        """
        try:
            # Try to create a connection pool to the Database
            cls.pool = await create_pool(
                user=SETTINGS.postgres_user,
                password=SETTINGS.postgres_pwd,
                database=SETTINGS.postgres_db,
                host=SETTINGS.postgres_host,
                port=SETTINGS.postgres_port,
                max_size=SETTINGS.connection_number,
            )

        except InvalidCatalogNameError:
            # Flag that indicates if the tables must be created
            create_tables = True
            # Connect to Database template
            sys_conn = await connect(
                host=SETTINGS.postgres_host,
                user=SETTINGS.postgres_user,
                port=SETTINGS.postgres_port,
                password=SETTINGS.postgres_pwd,
                database="template1",
            )
            try:
                # Create Database
                await sys_conn.execute(CREATE_DATABASE)

            except DuplicateDatabaseError:
                # Another process created the database so set create_tables to False
                create_tables = False

            finally:
                # Disconnect from database template
                await sys_conn.close()

            # Create a connection pool to the Database
            cls.pool = await create_pool(
                user=SETTINGS.postgres_user,
                password=SETTINGS.postgres_pwd,
                database=SETTINGS.postgres_db,
                host=SETTINGS.postgres_host,
                port=SETTINGS.postgres_port,
                max_size=SETTINGS.connection_number,
            )

            # Check if the tables must be created
            if create_tables:
                async with cls.pool.acquire() as connection:
                    # Create tables
                    await cls.__create_table_service_mapping(connection)
                    await cls.__create_table_device_mapping(connection)

    @classmethod
    async def insert_device(
        cls, keycloak_identifier: str, device: Device, username: str
    ):
        """
        Insert device in the database

        :param keycloak_identifier: uuid associated to the mapping
        :param device: Device to store
        :param username: client
        """
        try:
            async with cls.pool.acquire() as connection:
                await connection.execute(
                    INSERT["device"],
                    *(
                        keycloak_identifier,
                        device.device_id,
                        username,
                        device.json(exclude_none=True),
                    ),
                )

        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Device",
                    "status": "Something went wrong storing the data",
                },
            )

    @classmethod
    async def update_device(cls, device: Device, username: str):
        """
        Update device mapping

        :param device: device to update
        :param username: client
        """
        try:
            async with cls.pool.acquire() as connection:
                await connection.execute(
                    UPDATE["device"],
                    *(device.json(exclude_none=True), device.device_id, username),
                )
        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Device",
                    "status": "Something went wrong updating the data",
                },
            )

    @classmethod
    async def delete_device(cls, device_id: str, username: str):
        """
        Delete device from the database

        :param device_id: device identifier
        :param username: client
        """
        try:
            async with cls.pool.acquire() as connection:
                await connection.execute(DELETE["device"], *(device_id, username))
        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Device",
                    "status": "Something went wrong deleting the data",
                },
            )

    @classmethod
    async def extract_device(cls, device_id: str) -> Device:
        """
        Extract device info

        :param device_id: Device identifier
        :return: requested device
        """
        try:
            async with cls.pool.acquire() as conn:
                device_json = await conn.fetchval(SELECT["device"], device_id)
                if device_json is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="device not found"
                    )
                return Device.parse_raw(device_json)
        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Device",
                    "status": "Something went wrong extracting the data",
                },
            )

    @classmethod
    async def extract_all_devices(
        cls, keycloak_identifier: str, username: str
    ) -> List[Device]:
        """
        Extract all devices associated to the user

        :param keycloak_identifier: identifier of the user stored in keycloak
        :param username: user
        :return: User device list
        """
        try:
            async with cls.pool.acquire() as conn:
                device_list = await conn.fetch(
                    SELECT["device_list"], *(username, keycloak_identifier)
                )
                return [
                    Device.parse_raw(device["policy_list"])
                    for device in device_list
                    if device["policy_list"]
                ]
        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Device",
                    "status": "Something went extracting the data",
                },
            )

    @classmethod
    async def insert_service(
        cls, keycloak_identifier: str, username: str, service: Service
    ):
        """
        Insert service in the database

        :param keycloak_identifier: keycloak identifier
        :param username: client
        :param service: service
        """
        try:
            async with cls.pool.acquire() as connection:
                await connection.execute(
                    INSERT["service"],
                    *(
                        keycloak_identifier,
                        service.name,
                        username,
                        service.json(exclude_none=True),
                    ),
                )

        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Service",
                    "status": "Something went wrong storing the data",
                },
            )

    @classmethod
    async def update_service(cls, service: Service, username: str):
        """
        Update device mapping

        :param service: service to update
        :param username: client
        """
        try:
            async with cls.pool.acquire() as connection:
                await connection.execute(
                    UPDATE["service"],
                    *(service.json(exclude_none=True), service.name, username),
                )
        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Service",
                    "status": "Something went wrong updating the data",
                },
            )

    @classmethod
    async def extract_service_keycloak_identifier(
        cls, service_id: str, username: str
    ) -> str:
        """
        Extract keycloak identifier associated to the service
        :param service_id: Service of interest
        :param username: client
        :return: keycloak identifier
        """
        try:
            async with cls.pool.acquire() as connection:
                return await connection.fetchval(
                    SELECT["service_keycloak_id"],
                    *(
                        service_id,
                        username,
                    ),
                )

        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Service",
                    "status": "Something went wrong extracting the data",
                },
            )

    @classmethod
    async def extract_all_services(cls, username: str) -> List[Service]:
        """
        Extract all services associated to the user

        :param username: user
        :return: Service list
        """
        try:
            async with cls.pool.acquire() as connection:
                service_list = await connection.fetch(
                    SELECT["service_list"],
                    username,
                )
                return [
                    Service.parse_raw(service["policy_list"])
                    for service in service_list
                    if service["policy_list"]
                ]

        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Service",
                    "status": "Something went wrong extracting the data",
                },
            )

    @classmethod
    async def delete_service(cls, service_id: str, username: str):
        """
        Delete device from the database

        :param service_id: service identifier
        :param username: client
        """
        try:
            async with cls.pool.acquire() as connection:
                await connection.execute(DELETE["service"], *(service_id, username))
        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Service",
                    "status": "Something went wrong deleting the data",
                },
            )

    @classmethod
    async def filter_service_list(
        cls, gateway_service: GatewayService
    ) -> List[Optional[Service]]:
        """
        Extract a list of service from the database

        :param gateway_service: message to be routed by the gateway towards the services
        :return: Services requested
        """

        try:
            service_list = []
            async with cls.pool.acquire() as connection:
                for service_id in gateway_service.service_list:
                    service_json = await connection.fetchval(
                        SELECT["policy_list"], service_id
                    )
                    if service_json is None:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"service {service_id} not found",
                        )
                    service = Service.parse_raw(service_json)
                    service_scopes_set = set(service.resource_scopes)
                    control_flag = True
                    if "storage_policy" in service_scopes_set:
                        service_scopes_set = service_scopes_set.difference(
                            {"storage_policy"}
                        )
                        if gateway_service.sign_device.storage_policy:
                            if (
                                gateway_service.sign_device.storage_policy.timestamp()
                                < time.time()
                            ):
                                control_flag = False
                        else:
                            control_flag = False

                    if control_flag:
                        if service_scopes_set.issubset(
                            set(gateway_service.sign_device.policy_list)
                        ):
                            service_list.append(service)
            return service_list
        except PostgresError as error:
            await log_postgres_error(error)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "resource": "Service",
                    "status": "Something went wrong storing the data",
                },
            )

    @classmethod
    async def disconnect(cls):
        """
        Disconnect from the database
        """
        await cls.pool.close()


# ---------------------------------------------------------------------------------------


@lru_cache(maxsize=1)
def get_database() -> DataBase:
    """Obtain as a singleton an instance of the database"""
    return DataBase()


# ---------------------------------------------------------------------------------------
