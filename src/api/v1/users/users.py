from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query

from api.deps import CurrentActiveUser, get_current_admin
from core.container import Container
from schemas.response import Message
from schemas.response import PaginationResponse
from schemas.user import (
    UserResponse,
    UserParams,
    PasswordResetRequest,
    PasswordResetConfirm
)
from services.user import IUserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/me",
    response_model=UserResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Bad credentials",
        }
    }
)
@inject
async def get_me(user: CurrentActiveUser):
    return user


@router.get(
    path="/",
    response_model=PaginationResponse[UserResponse],
    dependencies=[Depends(get_current_admin)],
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden",
        }
    }
)
@inject
async def get_users(
        params: Annotated[UserParams, Query()],
        user_service: IUserService = Depends(Provide[Container.user_service])
):
    return await user_service.get_users(params=params)


@router.post(
    path="/password/reset",
    response_model=Message,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        }
    }
)
@inject
async def reset_password(
        schema: PasswordResetRequest,
        user_service: IUserService = Depends(Provide[Container.user_service])
):
    return await user_service.reset_password(schema=schema)


@router.post(
    path="/password/reset/confirm",
    response_model=Message,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid token",
        }
    }
)
@inject
async def confirm_password_reset(
        schema: PasswordResetConfirm,
        user_service: IUserService = Depends(Provide[Container.user_service])
):
    return await user_service.confirm_reset_password(schema=schema)
