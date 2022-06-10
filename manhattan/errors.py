# Manhattan
# Copyright (c) 2021-2022 Venera, Inc. All Rights Reserved.
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
