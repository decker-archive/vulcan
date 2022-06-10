# Manhattan
# Copyright (c) 2021-2022 Venera, Inc. All Rights Reserved.
from fastapi import Request
from .tokenize import verify_token
from .database import User
from .errors import BadData, HTTPError, Unauthorized


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
