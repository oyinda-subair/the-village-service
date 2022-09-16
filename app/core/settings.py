import logging
import os
import pathlib

from pydantic import BaseSettings, EmailStr
from dotenv import load_dotenv
from os.path import join
from .config import Config


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

dotenv_path = join(ROOT, '.env')
load_dotenv(dotenv_path)


class DBSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Config.DATABASE_URI
    FIRST_SUPERUSER: EmailStr = os.environ.get("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PW: str = os.environ.get("FIRST_SUPERUSER_PW")


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = Config.JWT_SECRET
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TEST_FLAG = os.environ.get("TEST_FLAG")

    logging: LoggingSettings = LoggingSettings()
    db: DBSettings = DBSettings()

    class Config:
        case_sensitive = True


settings = Settings()
