from loguru import logger
from typing import List

from fastapi import Depends
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from app.api import deps
from app.core.exception_handler import CustomException
from app.models.user import User


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(deps.get_current_user)):
        if not user:
            logger.error("🚫 AccessDenied: Not Authenticated")
            raise CustomException(
                code=HTTP_403_FORBIDDEN, message="Not authenticated"
            )

        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise CustomException(
                code=HTTP_401_UNAUTHORIZED,
                message=f"{user.email} is not authorized to access this endpoint")
