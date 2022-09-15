import os
import pathlib
from typing import get_type_hints, Union
from dotenv import load_dotenv
from os.path import join

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

dotenv_path = join(ROOT, '.env')
load_dotenv(dotenv_path)


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']

# AppConfig class with required fields, default values, type checking, and typecasting for int and bool values


class AppConfig:
    DEBUG: bool = False
    ENV: str = "production"
    DATABASE_URI: str = "postgres://"
    HOSTNAME: str
    PORT: int
    JWT_SECRET: str

    """
    Map environment variables to class fields according to these rules:
      - Field won't be parsed unless it has a type annotation
      - Field will be skipped if not in all caps
      - Class field and environment variable name are the same
    """

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            # Raise AppConfigError if required field not supplied
            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {} field is required'.format(field))

            # Cast env var value to expected type and raise AppConfigError on failure
            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError:
                raise AppConfigError('Unable to cast value of "{}" to type "{}" for "{}" field'.format(
                    env[field],
                    var_type,
                    field
                )
                )

    def __repr__(self):
        return str(self.__dict__)


# Expose Config object for app to import
Config = AppConfig(os.environ)
