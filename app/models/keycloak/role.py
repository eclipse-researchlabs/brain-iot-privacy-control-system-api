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
from typing import List

# Third Party
from orjson import loads
from pydantic import parse_raw_as

# Internal
from ..model import OrjsonModel

# -----------------------------------------------------------------------------


class RoleName(OrjsonModel):
    name: str = ...


def parse_roles(data: bytes) -> List[str]:
    """
    Parse client roles from data

    :param data: data to parse
    """
    role_list = parse_raw_as(List[RoleName], data, json_loads=loads)
    return [role.name for role in role_list if role.name != "uma_protection"]
