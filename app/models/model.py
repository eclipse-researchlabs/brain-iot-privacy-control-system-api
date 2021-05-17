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

# Third Party
import orjson
from pydantic import BaseModel

# --------------------------------------------------------------------------------------------


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class OrjsonModel(BaseModel):
    """Model that use orjson to serialize and deserialize"""

    class Config:
        # Use orjson to improve performance
        json_loads = orjson.loads
        json_dumps = orjson_dumps
