from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Query

from api.deps import CurrentActiveUser, get_current_admin
from core.container import Container
from domain.usecases import IUserUseCase
from schemas.response import Message, APIResponse
from schemas.response import PaginationResponse
from schemas.user import (
    UserResponse,
    UserParams,
    PasswordResetRequest,
    PasswordResetConfirm
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    path="/me",
    response_model=APIResponse[UserResponse],
    response_model_exclude_none=True,
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
    return APIResponse(
        ok=True,
        result=user
    )


@router.get(
    path="/",
    response_model=APIResponse[PaginationResponse[UserResponse]],
    response_model_exclude_none=True,
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
        user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case])
):
    result = await user_use_case.get_users(params=params)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/password/reset",
    response_model=APIResponse[Message],
    response_model_exclude_none=True,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        }
    }
)
@inject
async def reset_password(
        schema: PasswordResetRequest,
        user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case])
):
    result = await user_use_case.reset_password(schema=schema)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/password/reset/confirm",
    response_model=APIResponse[Message],
    response_model_exclude_none=True,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid token",
        }
    }
)
@inject
async def confirm_password_reset(
        schema: PasswordResetConfirm,
        user_use_case: IUserUseCase = Depends(Provide[Container.user_use_case])
):
    result = await user_use_case.confirm_reset_password(schema=schema)
    return APIResponse(
        ok=True,
        result=result
    )
