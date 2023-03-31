from typing import Any
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

from app import controller
from app import schemas
from app.api import deps
from app.core.init_logger import logger
from app.core.exception_handler import CustomException
from app.models.user import User
from loguru import logger

from app.schemas.user import ShortUserResponse


router = APIRouter()


@router.get("/me", response_model=schemas.ShortUserResponse)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    user = current_user
    data = ShortUserResponse(
        first_name=user.first_name,
        surname=user.surname,
        email=user.email,
        is_superuser=user.is_superuser,
        role=user.role
    )
    return data


@router.put("/{user_id}", response_model=schemas.User, status_code=200)
def user_update(
        *, db: Session = Depends(deps.get_db),
        user_id: str,
        user_in: schemas.UserUpdate, current_user: User = Depends(deps.get_current_user)) -> Any:
    user = _get_user(db, uuid.UUID(user_id), current_user.id)
    updated_user = controller.user.update(db=db, db_obj=user, obj_in=user_in)
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete_user(
        *, db: Session = Depends(deps.get_db),
        user_id: str, current_user: User = Depends(deps.get_current_user)) -> Any:
    _ = _get_user(db, uuid.UUID(user_id), current_user.id)
    return controller.user.delete(db=db, id=uuid.UUID(user_id))


def _get_user(db: Session, id: uuid.UUID, current_user_id: uuid.UUID) -> Any:
    user = controller.user.get(db, id=current_user_id)
    if not user:
        logger.error(f"User with ID: {current_user_id} not found.")
        raise CustomException(
            status.HTTP_404_NOT_FOUND, f"User with ID: {current_user_id} not found."
        )

    if id != current_user_id:
        logger.error(f"You can only update your profile.")
        raise CustomException(
            status.HTTP_403_FORBIDDEN, f"You can only update your profile."
        )
    return user
