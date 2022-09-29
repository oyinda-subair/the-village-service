from fastapi import APIRouter, Depends

from app.api.v1 import user
from app.api.v1 import admin
from app.api import deps

SUPERUSER_PROTECTED = Depends(deps.get_current_active_superuser)

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"],   dependencies=[SUPERUSER_PROTECTED])
