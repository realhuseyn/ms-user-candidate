import uuid
from typing import List

from fastapi import (APIRouter, Body, Depends, HTTPException, Request,
                     Response, status)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.controllers.controller.deps import get_current_user
from app.controllers.controller.schemas import User, UserUpdate
from app.utils.utils import get_hashed_password

user_router = APIRouter()


@user_router.get("/user", response_description="List all users", response_model=List[User], tags=["User Controller"])
async def list_users(request: Request, user: User = Depends(get_current_user)):
    users = list(request.app.database["users"].find())
    return users


@user_router.get("/user/{id}", response_description="Get a single user by id", response_model=User, tags=["User Controller"])
async def find_user(id: str, request: Request, user: User = Depends(get_current_user)):
    if (user := request.app.database["users"].find_one({"uuid": id})) is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {id} not found")


@user_router.post(
    "/user",
    response_description="Create a new user",
    status_code=status.HTTP_201_CREATED, response_model=User, tags=["User Controller"])
async def create_user(
        request: Request, user: User = Body(...), _user: User = Depends(get_current_user)) -> JSONResponse:
    if (request.app.database["users"].find_one({"email": user.email})) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user.uuid = str(uuid.uuid4())
    user.password = await get_hashed_password(user.password)
    user = jsonable_encoder(user)
    request.app.database["users"].insert_one(user)
    return user


@user_router.put("/user/{id}", response_description="Update a user", response_model=User, tags=["User Controller"])
async def update_user(id: str, request: Request, user: UserUpdate = Body(...), _user: User = Depends(get_current_user)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        request.app.database["users"].update_one(
            {"uuid": id}, {"$set": user}
        )

    if (
        existing_user := request.app.database["users"].find_one({"uuid": id})
    ) is not None:
        return existing_user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {id} not found")


@user_router.delete("/user/{id}", response_description="Delete a user", tags=["User Controller"])
async def delete_user(id: str, request: Request, response: Response, user: User = Depends(get_current_user)):
    delete_result = request.app.database["users"].delete_one(
        {"uuid": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {id} not found")


@user_router.get('/me', summary='Get details of currently logged in user', response_model=User, tags=["User Controller"])
async def get_me(user: User = Depends(get_current_user)):
    return user
