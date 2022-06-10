from fastapi import FastAPI, Request

from manhattan.errors import BadData, HTTPError
from manhattan.utils import jsonify
from manhattan.database import connect

# routes
from manhattan.users import users_router

app = FastAPI()

app.include_router(users_router)

@app.exception_handler(HTTPError)
async def httperror(_, err: HTTPError):
    resp = jsonify(err._to_dict(), err.HTTP_CODE)

    if err._delete_cookies:
        for cookie in err._delete_cookies:
            resp.delete_cookie(cookie, secure=True)

    return resp

@app.exception_handler(404)
async def notfound(*_):
    err = HTTPError(custom_msg='Not Found')
    err.HTTP_CODE = 404
    return await httperror(None, err=err)

@app.exception_handler(KeyError)
async def baddata(*_):
    err = BadData()
    return await httperror(None, err=err)

@app.on_event('startup')
async def on_startup():
    connect()

