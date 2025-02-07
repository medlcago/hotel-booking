from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from api.deps import CurrentUser, RefreshTokenResult
from core.container import Container
from domain.usecases import IAuthUseCase
from schemas.auth import (
    SignUpRequest,
    SignInRequest,
    ConfirmEmailRequest,
)
from schemas.response import Message, APIResponse
from schemas.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/confirmation-code",
    response_model=APIResponse[Message],
    response_model_exclude_none=True,
)
@inject
async def send_confirmation_code(
        user: CurrentUser,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    result = await auth_use_case.send_confirmation_code(email=user.email)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/confirm-email",
    response_model=APIResponse[Message],
    response_model_exclude_none=True,
)
@inject
async def confirm_email(
        schema: ConfirmEmailRequest,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    result = await auth_use_case.confirm_email(schema=schema)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/sign-up",
    response_model=APIResponse[Token],
    response_model_exclude_none=True,
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
    result = await auth_use_case.sign_up(schema=schema)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/sign-in",
    response_model=APIResponse[Token],
    response_model_exclude_none=True,
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
    result = await auth_use_case.sign_in(schema=schema)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/refresh-token",
    response_model=APIResponse[Token],
    response_model_exclude_none=True,
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
        token: RefreshTokenResult,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    result = await auth_use_case.refresh_token(token=token)
    return APIResponse(
        ok=True,
        result=result
    )


@router.post(
    path="/logout",
    response_model=APIResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
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
        token: RefreshTokenResult,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    result = await auth_use_case.revoke_token(token=token)
    return APIResponse(
        ok=True,
        result=result
    )
