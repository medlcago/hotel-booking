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
    status_code=status.HTTP_201_CREATED
)
@inject
async def sign_up(
        schema: SignUpRequest,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.register(schema=schema)


@router.post(path="/sign-in", response_model=Token)
@inject
async def sign_in(
        schema: SignInRequest,
        auth_use_case: IAuthUseCase = Depends(Provide[Container.auth_use_case])
):
    return await auth_use_case.login(schema=schema)


@router.post("/refresh-token", response_model=Token)
async def refresh_token(token: RefreshToken):
    # TODO implement logic
    pass
