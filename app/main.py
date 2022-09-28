import time
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse

from app.api.routes import api_router
from app.core.settings import settings
from app.core.init_logger import setup_app_logging
from app.core.exception_handler import CustomException

setup_app_logging(config=settings)
root_router = APIRouter()
app = FastAPI(title="The Village API", openapi_url=f"{settings.API_V1_STR}/openapi.json")


@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"Exception Occurred! Reason -> {exc.message}"},
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
