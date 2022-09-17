from fastapi import FastAPI, APIRouter

from app.api.routes import api_router
from app.core.settings import settings
from app.core.init_logger import setup_app_logging

setup_app_logging(config=settings)
root_router = APIRouter()
app = FastAPI(title="The Village API", openapi_url=f"{settings.API_V1_STR}/openapi.json")


@root_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
