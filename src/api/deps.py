from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from core.container import ServiceContainer
from core.exceptions import UnauthorizedException, ForbiddenException
from core.security import JWTBearer
from models import User
from schemas.user import UserResponse
from services.user import IUserService

jwt_bearer = JWTBearer()


@inject
async def get_current_user(
        identity: int = Depends(jwt_bearer),
        user_service: IUserService = Depends(Provide[ServiceContainer.user_service]),
) -> UserResponse:
    user = await user_service.get_user_by_id(user_id=identity)
    if not user:
        raise UnauthorizedException
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def get_current_admin(user: CurrentUser) -> User:
    if not user.is_admin:
        raise ForbiddenException
    return user
