import os

from starlette.config import Config

project_name = "ms-user-candidate"


class BaseConfig:

    """
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments
    """
    config = Config()

    INCLUDE_SCHEMA = config("INCLUDE_SCHEMA", cast=bool, default=True)

    SECRET_KEY = config("SECRET_KEY", default=os.urandom(32))

    CORS_ORIGINS = config("CORS_HOSTS", default="*")

    DEBUG = config("DEBUG", cast=bool, default=True)
    TESTING = config("TESTING", cast=bool, default=False)

    SERVICE_NAME = "ms-user-candidate"
    API_VERSION = "v1"
    BASE_URL = f"/{project_name}/{API_VERSION}"
