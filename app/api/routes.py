from fastapi import APIRouter, Depends

from app.api.v1 import admin
from app.api.v1 import auth
from app.api.v1 import comment
from app.api.v1 import post
from app.api.v1 import user
from app.core.provider.role_checker import RoleChecker

ALLOW_CREATE_RESOURCE = RoleChecker(["admin"])

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(
    admin.router, prefix="/admin", tags=["admin"],
    dependencies=[Depends(ALLOW_CREATE_RESOURCE)])
api_router.include_router(post.router, prefix="/posts", tags=["posts"])
api_router.include_router(comment.router, prefix="/comments", tags=["comments"])
