from typing import Any
import uuid
from fastapi import Depends, status
from loguru import logger
from sqlalchemy.orm.session import Session

from app.api import deps
from app.core.exception_handler import CustomException
from app.models.user import User


class PreviledgeChecker:
    async def owner_can_make_update(db: Session, user_id: uuid.UUID, current_user: str = Depends(deps.get_current_user)) -> User:
        if not current_user:
            logger.error(f"User with ID: {current_user_id} not found.")
            raise CustomException(
                status.HTTP_404_NOT_FOUND, f"User with ID: {current_user_id} not found."
            )

        current_user_id = current_user.id

        if user_id != current_user_id:
            logger.error(f"AccessDenied: You do not have access to modify this data.")
            raise CustomException(
                status.HTTP_403_FORBIDDEN, f"AccessDenied: You do not have access to modify this data."
            )
        return current_user
