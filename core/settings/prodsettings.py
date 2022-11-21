from starlette.config import Config
from starlette.datastructures import Secret

from core.settings.settings import BaseConfig


class ProdSettings(BaseConfig):

    """ Configuration class for site production environment """

    config = Config()
    DEBUG = False
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", cast=str, default="password123")
    JWT_REFRESH_SECRET_KEY = config(
        "JWT_REFRESH_SECRET_KEY", cast=str, default="password123")
    DB_USER = config("DB_USER", cast=str, default="postgres")
    DB_PASSWORD = config("DB_PASSWORD", cast=Secret, default="postgres")
    DB_HOST = config("DB_HOST", cast=str, default="db")
    DB_PORT = config("DB_PORT", cast=int, default="5432")
    DB_NAME = config("DB_NAME", cast=str, default="postgres")
    INCLUDE_SCHEMA = config("INCLUDE_SCHEMA", cast=bool, default=False)
    DATABASE_URL = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin"
