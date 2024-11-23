from dataclasses import dataclass

from core.exceptions import NotFoundException
from core.uow import IUnitOfWork
from schemas.user import UserResponse


@dataclass(frozen=True, slots=True)
class UserService:
    uow: IUnitOfWork

    async def get_user_by_email(self, email: str) -> UserResponse:
        async with self.uow:
            user = await self.uow.user_repository.get_user_by_email(email=email)
            if not user:
                raise NotFoundException
            return UserResponse.model_validate(user, from_attributes=True)

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        async with self.uow:
            user = await self.uow.user_repository.get_user_by_id(user_id=user_id)
            if not user:
                raise NotFoundException
            return UserResponse.model_validate(user, from_attributes=True)
