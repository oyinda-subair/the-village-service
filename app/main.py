from asyncio.log import logger
from email import message
import time
from fastapi import FastAPI, APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import ExceptionMiddleware

from app.api.routes import api_router
from app.core.settings import settings, ENV
from app.core.init_logger import setup_app_logging
from app.core.exception_handler import CustomException
import sys

sys.path.append('./../')
setup_app_logging(config=settings)
root_router = APIRouter()
app = FastAPI(title="The Village API", openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if settings.cors.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.cors.BACKEND_CORS_ORIGINS],
        allow_origin_regex=settings.cors.BACKEND_CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@root_router.get("/healthchecker", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!", "environment": ENV}


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder({
            "status_code": exc.code,
            "message": exc.message,
            "exception": f"Exception Occurred! Reason -> {exc.message}"
        }),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = jsonable_encoder({"detail": exc.errors(),
                                "body": exc.body})
    logger.error(f"OMG! The client sent invalid data!: {content}")
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
