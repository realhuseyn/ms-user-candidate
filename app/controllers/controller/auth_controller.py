
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers.controller.schemas import TokenSchema
from app.utils.utils import (create_access_token, create_refresh_token,
                             verify_password)

auth_router = APIRouter()


@auth_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema, tags=["Auth Controller"])
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = request.app.database["users"].find_one(
        {"email": form_data.username}) or None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not await verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": await create_access_token(user['email']),
        "refresh_token": await create_refresh_token(user['email']),
    }
