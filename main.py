# Manhattan
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
import sys
import os

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from dotenv import load_dotenv

from manhattan.database import connect
from manhattan.errors import BadData, HTTPError

# routes
from manhattan.users import users_router
from manhattan.utils import jsonify

from cassandra.cqlengine.query import DoesNotExist

load_dotenv()

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv('REDIS_URI'),
    default_limits=[
        '10/second'
    ],
    headers_enabled=True
)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.include_router(users_router)


@app.exception_handler(HTTPError)
async def httperror(_, err: HTTPError):
    print(err, file=sys.stderr)
    resp = jsonify(err._to_dict(), err.HTTP_CODE)

    if err._delete_cookies:
        for cookie in err._delete_cookies:
            resp.delete_cookie(cookie, secure=True)

    return resp


@app.exception_handler(404)
async def notfound(*_):
    print(_, file=sys.stderr)
    err = HTTPError(custom_msg='Not Found')
    err.HTTP_CODE = 404
    return await httperror(None, err=err)


@app.exception_handler(KeyError)
async def baddata(*_):
    print(_, file=sys.stderr)
    err = BadData()
    return await httperror(None, err=err)

@app.exception_handler(DoesNotExist)
async def doesnotexist(*_):
    return await baddata(*_)


@app.on_event('startup')
async def on_startup():
    connect()
