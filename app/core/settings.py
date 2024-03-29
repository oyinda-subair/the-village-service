import logging
import os
import pathlib
from typing import List, Optional, Union

from pydantic import BaseSettings, EmailStr, AnyHttpUrl, validator
from dotenv import load_dotenv
from os.path import join
from .config import Config


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

dotenv_path = join(ROOT, '.env')
load_dotenv(dotenv_path)


class DBSettings(BaseSettings):
    DATABASE_URL: str = Config.DATABASE_URL
    TEST_DATABASE_URL = os.environ.get("TEST_DB_URL")
    FIRST_SUPERUSER: EmailStr = os.environ.get("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PW: str = os.environ.get("FIRST_SUPERUSER_PW")


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO


class BackendCorsSetting(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:5173/",
    ]

    # Origins that match this regex OR are in the above list are allowed
    BACKEND_CORS_ORIGIN_REGEX: Optional[
        str
    ] = ""  # noqa: W605

    BACKEND_CORS_ALLOWED_METHODS: List[str] = ["OPTIONS", "POST", "PUT", "GET", "DELETE", "PATCH"]
    BACKEND_CORS_ALLOWED_HEADERS: List[str] = ["Origin", "Cache-Control", "Accept",
                                               "X-Access-Token", "X-Requested-With", "Content-Type", "Authorization"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = Config.JWT_SECRET
    ALGORITHM: str = "HS256"
    ENVIRONMENT: str = Config.ENVIRONMENT
    BASE_URL = "http://localhost:8001"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    logging: LoggingSettings = LoggingSettings()
    db: DBSettings = DBSettings()
    cors: BackendCorsSetting = BackendCorsSetting()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

RUNTIME_ENV = {
    "dev": "Development",
    "test": "Test",
    "prod": "Production"
}

ENV = RUNTIME_ENV[settings.ENVIRONMENT]
