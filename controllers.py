from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel

from db.connector import Db


class Controller:
    class User(BaseModel):
        NAME: str = ''
        EMAIL: str = ''

    def root(self):
        res = Db.make_query('SELECT NAME, EMAIL FROM `b_user`')
        return JSONResponse(res, status.HTTP_200_OK)

    def user(self, user_id: int):
        res = Db.make_query("SELECT NAME, EMAIL FROM `b_user` WHERE ID = %s", (user_id,))
        return JSONResponse(res, status.HTTP_200_OK)
