from asyncio.log import logger
import time
from fastapi import FastAPI, APIRouter, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import ExceptionMiddleware
# from starlette.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.settings import settings, ENV
from app.core.init_logger import setup_app_logging
from app.core.exception_handler import CustomException
import sys

sys.path.append('./../')
setup_app_logging(config=settings)


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


app = FastAPI(title="The Village API", openapi_url=f"{settings.API_V1_STR}/openapi.json", docs_url="/docs",
              redoc_url="/redoc", debug=True)

if settings.USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8001

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    settings.BASE_URL = public_url
    init_webhooks(public_url)


# ... Initialize routers and the rest of our app

root_router = APIRouter()


@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!", "environment": ENV}


@root_router.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = "http://localhost:5173"
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Authorization"
    response.headers['Access-Control-Max-Age'] = "600"
    return response


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    logger.error(f"Exception Occurred! Reason -> {exc.message}")
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

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)


@app.middleware("http")
async def cors_handler(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = "http://localhost:5173"
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers['Access-Control-Allow-Headers'] = "Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization, ngrok-skip-browser-warning"
    response.headers['Access-Control-Max-Age'] = "600"
    return response

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[str(origin) for origin in settings.cors.BACKEND_CORS_ORIGINS],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     max_age=3600
# )


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
