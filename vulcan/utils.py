# Vulcan
# Copyright (c) 2021-2022 Venera, Inc. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
from typing import Any

import orjson
from fastapi import Request, Response


def jsonify(d: Any, status: int = 200):
    return Response(orjson.dumps(d), status_code=status, media_type='application/json')


async def get_data(req: Request):
    body = await req.body()
    return orjson.loads(body)
