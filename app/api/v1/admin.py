from typing import List, Any
import uuid
from fastapi import APIRouter, Depends, status

from app import controller
from app import schemas
from app.api import deps
from app.core.exception_handler import CustomException
from app.schemas.common import DataResponseModel

from sqlalchemy.orm.session import Session
from loguru import logger

router = APIRouter()


# GET admin/users/ (all users)
@router.get("/users", response_model=DataResponseModel[List[schemas.User]], status_code=200)
def fetch_all_users(
        skip: int = 0, limit: int = 100,
        *,
        db: Session = Depends(deps.get_db)) -> Any:
    users = controller.admin.get_multi(db, skip=skip, limit=limit)
    return DataResponseModel(success=True, data=users)

# GET admin/user/:id


@router.get("/user/{user_id}", response_model=DataResponseModel[schemas.User], status_code=200)
def fetch_user(
        *, db: Session = Depends(deps.get_db),
        user_id: str) -> Any:
    user = controller.admin.get(db, uuid.UUID(user_id))
    return DataResponseModel(success=True, data=user)

# PUT admin/user/:id


@router.put("/user/{user_id}", response_model=schemas.User, status_code=200)
def user_update(
        *, db: Session = Depends(deps.get_db),
        user_id: str,
        user_in: schemas.UserUpdate) -> Any:
    user = _get_user(db, uuid.UUID(user_id))

    updated_user = controller.user.update(db=db, db_obj=user, obj_in=uuid.UUID(user_in))
    return updated_user

# DELETE admin/user/:id


@router.delete("/user/{user_id}", status_code=204)
def delete_user(
        *, db: Session = Depends(deps.get_db),
        user_id: str) -> Any:
    _ = _get_user(db, uuid.UUID(user_id))
    return controller.user.delete(db=db, id=uuid.UUID(user_id))


def _get_user(db: Session, user_id: uuid.UUID) -> Any:
    user = controller.user.get(db, id=user_id)
    if not user:
        logger.error(f"User with ID: {user_id} not found.")
        raise CustomException(
            status.HTTP_404_NOT_FOUND, f"User with ID: {user_id} not found."
        )

    return user
