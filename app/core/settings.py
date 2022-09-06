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


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Config.DATABASE_URI
    FIRST_SUPERUSER: EmailStr = os.environ.get("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PW: str = os.environ.get("FIRST_SUPERUSER_PW")

    class Config:
        case_sensitive = True


settings = Settings()
