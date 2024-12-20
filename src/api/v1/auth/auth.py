from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from api.deps import CurrentUser, RefreshTokenResult
from core.container import Container
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
        auth_service: IAuthService = Depends(Provide[Container.auth_service])
):
    return await auth_service.send_confirmation_email(email=user.email)


@router.get(
    path="/confirm-email",
    response_model=Message
)
@inject
async def confirm_email(
        token: str,
        auth_service: IAuthService = Depends(Provide[Container.auth_service])
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
        auth_service: IAuthService = Depends(Provide[Container.auth_service])
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
        auth_service: IAuthService = Depends(Provide[Container.auth_service])
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
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "The token has expired",
        }
    }
)
@inject
async def refresh_token(
        result: RefreshTokenResult,
        auth_service: IAuthService = Depends(Provide[Container.auth_service])
):
    return await auth_service.refresh_token(result=result)


@router.post(
    path="/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid token",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "The token has expired",
        }
    }
)
@inject
async def logout(
        result: RefreshTokenResult,
        auth_service: IAuthService = Depends(Provide[Container.auth_service])
):
    await auth_service.revoke_token(result=result)
