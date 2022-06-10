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
class HTTPError(Exception):
    HTTP_CODE = 500
    HTTP_MESSAGE = 'Internal Server Error'

    def __init__(self, custom_msg: str = None, delete_cookies: list[str] = None, *args):
        if custom_msg:
            self.HTTP_MESSAGE = custom_msg

        self._args = args
        self._delete_cookies = delete_cookies

    def _to_dict(self):
        ret = {
            'message': '{}: {}'.format(str(self.HTTP_CODE), self.HTTP_MESSAGE),
            'code': 0,
        }

        if self.args != ():
            ret['reports'] = list(self.args)

        return ret


class Forbidden(HTTPError):
    HTTP_CODE = 403
    HTTP_MESSAGE = 'Forbidden'

class Unauthorized(HTTPError):
    HTTP_CODE = 401
    HTTP_MESSAGE = 'Unauthorized'

class BadData(HTTPError):
    HTTP_CODE = 400
    HTTP_MESSAGE = 'Bad Data'
