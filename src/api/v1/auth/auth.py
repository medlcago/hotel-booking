from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from core.container import Container
from schemas.auth import (
    SignUpRequest,
    SignInRequest
)
from schemas.token import Token, RefreshToken
from use_cases.auth import IAuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/sign-up",
    response_model=Token,
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
    return await auth_use_case.register(schema=schema)


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
    return await auth_use_case.login(schema=schema)


@router.post(
    path="/refresh-token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid token",
        }
    }
)
@inject
async def refresh_token(
        schema: RefreshToken,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.refresh_token(schema=schema)
