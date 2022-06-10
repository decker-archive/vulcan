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
from fastapi import Request

from .database import User
from .errors import BadData, HTTPError, Unauthorized
from .tokenize import verify_token


def authorize(req: Request):
    try:
        token = req.cookies['authorization']
    except:
        raise Unauthorized()
    try:
        return verify_token(token=token)
    except HTTPError as exc:
        exc._delete_cookies = ['authorization']
        raise exc


def verify_email(email: str):
    try:
        User.objects(User.email == email).allow_filtering().get()
    except:
        return email
    else:
        raise BadData(custom_msg='Email is already registered')
