from typing import Annotated
from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.exc import NoResultFound, InterfaceError, IntegrityError


from schemas import User as UserSchema
from .crud import UsersCRUD
from .dependencies import users_crud

DEFAULT_STR = ""
DEFAULT_EMAIL = "***@***.***"
DEFAULT_PHONE = "+7**********"

router = APIRouter(tags=["Users"], prefix="/users")


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Create user",
    responses={
        status.HTTP_200_OK: {
            "description": "User created",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User created",
                        "user info": {
                            "username": "string",
                            "first_name": "",
                            "last_name": "",
                            "email": "user@example.com",
                            "phone": "string",
                            "password": "stringst",
                        },
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def set_user(
    user_in: Annotated[UserSchema, Body()],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Создание нового пользователя
    """
    try:
        user = await crud.create(user_in)
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "User already exists"},
        )
    return {
            "description": "User created",
            "user info": user,
        }



@router.get(
    "/all_users",
    status_code=status.HTTP_200_OK,
)
async def all_users(
        crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Получаем всех имеющихся пользователей.
    """
    try:
        users = await crud.get()
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return users

