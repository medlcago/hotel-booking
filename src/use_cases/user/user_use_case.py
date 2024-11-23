from dataclasses import dataclass

from schemas.pagination import PaginationResponse
from schemas.user import UserParams, UserResponse
from services.user import IUserService


@dataclass(frozen=True, slots=True)
class UserUseCase:
    user_service: IUserService

    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        users = await self.user_service.get_users(params=params)
        return users
