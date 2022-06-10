# Manhattan
# Copyright (c) 2021-2022 Venera, Inc. All Rights Reserved.
from typing import Any

import orjson

from fastapi import Response, Request

def jsonify(d: Any, status: int = 200):
    return Response(
        orjson.dumps(d),
        status_code=status,
        media_type='application/json'
    )

async def get_data(req: Request):
    body = await req.body()
    return orjson.loads(body)

