from dataclasses import dataclass

from services.user import IUserService


@dataclass(frozen=True, slots=True)
class UserUseCase:
    user_service: IUserService
