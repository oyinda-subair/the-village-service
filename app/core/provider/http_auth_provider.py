from loguru import logger
from sqlalchemy.orm.session import Session
from typing import Set, List

from fastapi import Depends, Header
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from app.api import deps
from app.core.exception_handler import CustomException
from app.models.user import User


class HTTPHeaderAuthentication:
    def __init__(self, *, scopes: List[str]):
        self.scopes = set(scopes)

    async def __call__(self, request: Request, authuser: str = Header(None)) -> User:
        user = self.locate_user(username=authuser)
        if not user:
            raise CustomException(
                code=HTTP_403_FORBIDDEN, message="Not authenticated"
            )
        if not self.has_required_scope(user.roles):
            raise CustomException(
                code=HTTP_401_UNAUTHORIZED,
                message=f"{user.email} is not authorized to access this endpoint")
        return user

    def locate_user(self, current_user: User = Depends(deps.get_current_user)) -> User:
        return current_user

    def has_required_scope(self, user_scopes: Set[str]) -> bool:
        """Verify the user has the desired auth scope"""
        for scope in self.scopes:
            if scope not in user_scopes:
                return False
        return True
