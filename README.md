# FastAPI + MySQL + Redis

Integration example

https://github.com/tiangolo/fastapi

## Setup

```
$ git clone https://github.com/Uru-ruru/fastapi-mysql-integration
$ cd fastapi-mysql-integration/
$ sudo pip3 install -r requirements.txt
```

Add .env params

```
DBHOST=localhost
DBUSER=bitrix
DBPASS=bitrix
DBNAME=bitrix
REDISHOST=localhost
REDISTTL=600
REDISPASS=1234567
```

## Run

```
$ uvicorn main:app --reload
```

## Use

```
GET https://{{host}}/
Accept: application/json
```

1. Add queries to Controller (Bitrix user table Example)

```python
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
```
2. Add route to API

```python
@app.get("/", response_model=controller.User, response_model_exclude_unset=True)
async def root():
    return controller.root()


@app.get("/user/{user_id}", response_model=controller.User, response_model_exclude_unset=True)
async def hello(user_id: int):
    return controller.user(user_id)
```

3. Get access to swagger http://127.0.0.1:8000/docs 