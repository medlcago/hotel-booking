from dataclasses import dataclass

from core.exceptions import NotFoundException
from repositories.user import IUserRepository
from schemas.pagination import PaginationResponse
from schemas.user import UserResponse, UserParams


@dataclass(frozen=True, slots=True)
class UserService:
    user_repository: IUserRepository

    async def get_user_by_email(self, email: str) -> UserResponse:
        user = await self.user_repository.get_user_by_email(email=email)
        if not user:
            raise NotFoundException
        return UserResponse.model_validate(user, from_attributes=True)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id=user_id)
        if not user:
            raise NotFoundException
        return UserResponse.model_validate(user, from_attributes=True)

    async def get_users(self, params: UserParams) -> PaginationResponse[UserResponse]:
        users = await self.user_repository.get_users(**params.model_dump(exclude_none=True))
        return PaginationResponse[UserResponse].model_validate(
            users,
            from_attributes=True
        )
