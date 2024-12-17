from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from api.deps import refresh_token_bearer, CurrentUser
from core.container import ServiceContainer
from schemas.auth import (
    SignUpRequest,
    SignInRequest,
)
from schemas.response import Message
from schemas.token import Token
from schemas.user import UserResponse
from services.auth import IAuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/confirm-email",
    response_model=Message
)
@inject
async def send_confirmation_email(
        user: CurrentUser,
        auth_service: IAuthService = Depends(Provide[ServiceContainer.auth_service])
):
    return await auth_service.send_confirmation_email(email=user.email)


@router.get(
    path="/confirm-email",
    response_model=Message
)
@inject
async def confirm_email(
        token: str,
        auth_service: IAuthService = Depends(Provide[ServiceContainer.auth_service])
):
    return await auth_service.confirm_email(token=token)


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
        auth_service: IAuthService = Depends(Provide[ServiceContainer.auth_service])
):
    return await auth_service.sign_up(schema=schema)


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
        auth_service: IAuthService = Depends(Provide[ServiceContainer.auth_service])
):
    return await auth_service.sign_in(schema=schema)


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
        auth_service: IAuthService = Depends(Provide[ServiceContainer.auth_service])
):
    return await auth_service.refresh_token(user_id=user_id)
