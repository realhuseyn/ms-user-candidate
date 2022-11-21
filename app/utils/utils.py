import os
import uuid
from datetime import datetime, timedelta
from typing import Any, Union

from fastapi.encoders import jsonable_encoder
from jose import jwt
from passlib.context import CryptContext

import app.main
from app.controllers.controller.schemas import User
from core.factories import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


async def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_default_user():
    def_user = User(first_name='admin', last_name='admin',
                    email='admin@localhost.com', password='admin123')
    if (app.main.app.database["users"].find_one({"email": def_user.email})) is not None:
        print(f'Default username: {def_user.email}\tPassword: admin123')
        return
    print("Creating default user...")
    def_user.uuid = str(uuid.uuid4())
    def_user.password = await get_hashed_password(def_user.password)
    def_user.email
    def_user = jsonable_encoder(def_user)
    app.main.app.database["users"].insert_one(def_user)
    print(f'Default username: {def_user.email}\tPassword: admin123')
