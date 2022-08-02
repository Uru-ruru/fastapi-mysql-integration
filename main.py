from fastapi import FastAPI, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from controllers import Controller
from dotenv import load_dotenv
from starlette.exceptions import HTTPException as StarletteHTTPException

load_dotenv()

app = FastAPI(debug=True)
controller = Controller()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "status": exc.status_code,
            "detail": exc.detail
        }),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": exc.errors(),
            "body": exc.body
        }),
    )


@app.get("/", response_model=controller.User, response_model_exclude_unset=True)
async def root():
    return controller.root()


@app.get("/user/{user_id}", response_model=controller.User, response_model_exclude_unset=True)
async def hello(user_id: int):
    return controller.user(user_id)
