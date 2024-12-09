from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from api.deps import refresh_token_bearer, CurrentUser
from core.container import Container
from schemas.auth import (
    SignUpRequest,
    SignInRequest,
)
from schemas.response import Message
from schemas.token import Token
from schemas.user import UserResponse
from use_cases.auth import IAuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/confirm-email",
    response_model=Message
)
@inject
async def send_confirmation_email(
        user: CurrentUser,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.send_confirmation_email(email=user.email)


@router.get(
    path="/confirm-email",
    response_model=Message
)
@inject
async def confirm_email(
        token: str,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.confirm_email(token=token)


@router.post(
    path="/sign-up",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "User already exists",
        }
    }
)
@inject
async def sign_up(
        schema: SignUpRequest,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.register_user(schema=schema)


@router.post(
    path="/sign-in",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        }
    }
)
@inject
async def sign_in(
        schema: SignInRequest,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.login_user(schema=schema)


@router.post(
    path="/refresh-token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid token",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated",
        }
    }
)
@inject
async def refresh_token(
        user_id: int = Depends(refresh_token_bearer),
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.refresh_token(user_id=user_id)
