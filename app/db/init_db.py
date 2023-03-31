from sqlalchemy.orm import Session
from app.schemas.base import UserRole

import controller
import schemas
from db import base  # noqa: F401
from app.core.settings import settings
from loguru import logger


def init_db(db: Session) -> None:
    if settings.db.FIRST_SUPERUSER:
        user = controller.user.get_by_email(db, email=settings.db.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                first_name="Initial Super User",
                email=settings.db.FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.db.FIRST_SUPERUSER_PW,
                role=UserRole.ADMIN,
            )
            user = controller.user.create(db=db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.db.FIRST_SUPERUSER} already exists. "
            )
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=email@email.com"
        )
