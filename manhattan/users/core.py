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
import asyncio
import re

import bcrypt
from fastapi import APIRouter, Request

from ..checks import authorize, verify_email
from ..database import User, to_dict
from ..errors import BadData, Forbidden
from ..snowflakes import snowflake_factory
from ..tokenize import create_token as ctoken
from ..utils import get_data, jsonify

users_router = APIRouter(prefix='/api/users')


USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9\-_]{1,45}$')
LOCALES = [
    'en-US',
    'en-GB',
]


@users_router.get('/@me')
async def get_me(req: Request):
    return jsonify(to_dict(authorize(req=req)))


@users_router.get('/_auth/create-token')
async def create_token(req: Request):
    email = str(req.query_params.get('email'))
    password = str(req.query_params.get('password'))

    user = User.objects(User.email == email).allow_filtering().get()

    loop = asyncio.get_running_loop()
    valid_pw = await loop.run_in_executor(
        None, bcrypt.checkpw, password.encode(), user.password.encode()
    )

    if not valid_pw:
        raise Forbidden(custom_msg='Invalid Password')

    resp = jsonify({}, 201)
    resp.set_cookie('authorization', ctoken(user.id, user.password), secure=True)

    return resp


@users_router.post('')
async def create_user(request: Request):
    data: dict = await get_data(req=request)
    loop = asyncio.get_running_loop()

    if request.cookies.get('authorization'):
        raise BadData(custom_msg='Already logged into another account.')

    name = str(data['name'])

    if not USERNAME_REGEX.match(name):
        raise BadData(
            'name does not fit regex; "^[a-z0-9\-_]{3,45}$"', custom_msg='Invalid name'
        )

    password = await loop.run_in_executor(
        None, bcrypt.hashpw, str(data['password']).encode(), bcrypt.gensalt(17)
    )
    password = password.decode()

    locale = 'en-US'

    if data.get('locale'):
        if str(data['locale']) not in LOCALES:
            raise BadData(
                'Invalid locale',
                str(data['locale']) + ' is not a valid and/or usable locale.',
            )
        else:
            locale = str(data['locale'])

    screen_name = name

    if data.get('screen_name'):
        screen_name = str(data['screen_name'])

        if len(screen_name) > 45:
            raise BadData(
                'Max screen_name Length is 45', custom_msg='Invalid screen_name length'
            )

    email = str(data['email'])
    verify_email(email=email)

    if len(email) > 50:
        raise BadData('Max email Length is 50', custom_msg='Invalid email length')

    user: User = User.create(
        id=snowflake_factory.write(),
        email=email,
        password=password,
        name=name,
        screen_name=screen_name,
        locale=locale,
    )

    asdict = to_dict(user)

    response = jsonify(asdict, 201)

    response.set_cookie('authorization', ctoken(user.id, user.password), secure=True)

    return response
