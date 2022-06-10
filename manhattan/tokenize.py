# Manhattan
# Copyright (c) 2021-2022 Venera, Inc. All Rights Reserved.
import base64
import binascii

import itsdangerous
from fastapi import Request

from .database import User
from .errors import Forbidden, Unauthorized


def create_token(user_id: int, user_password: str) -> str:
    signer = itsdangerous.TimestampSigner(user_password)
    user_id = str(user_id)
    user_id = base64.b64encode(user_id.encode())

    return signer.sign(user_id).decode()


def verify_token(token: str):
    if token is None or not isinstance(token, str):
        raise Unauthorized()

    fragmented = token.split('.')
    username = fragmented[0]

    try:
        id = int(base64.b64decode(username.encode()))
    except (binascii.Error, ValueError):
        raise Unauthorized(custom_msg='Invalid ID in Token')

    try:
        user: User = User.objects(User.id == id).get()
    except:
        raise Unauthorized(custom_msg='Invalid user')

    signer = itsdangerous.TimestampSigner(user.password)

    try:
        signer.unsign(token)

        return user
    except (itsdangerous.BadSignature):
        raise Forbidden(custom_msg='Invalid token')


async def is_logged_in(req: Request) -> bool:
    return req.cookies.get('venera-oauth')


async def get_current_user(req: Request) -> User:
    if not await is_logged_in(req=req):
        raise Unauthorized(custom_msg='No Authorization')

    tok = req.cookies.get('venera-oauth')

    return verify_token(token=tok)
