from dataclasses import dataclass

from core import security
from core.exceptions import AlreadyExistsException
from core.exceptions import UnauthorizedException
from repositories.user import IUserRepository
from schemas.auth import SignInRequest
from schemas.auth import SignUpRequest
from schemas.token import Token


@dataclass(frozen=True, slots=True)
class AuthService:
    user_repository: IUserRepository

    async def sign_up(self, schema: SignUpRequest) -> Token:
        user = await self.user_repository.get_user_by_email(email=schema.email)
        if user:
            raise AlreadyExistsException

        schema.password = security.hash_password(schema.password)
        user = await self.user_repository.create_user(values=schema.model_dump())
        return self.get_token(
            user_id=user.id
        )

    async def sign_in(self, schema: SignInRequest) -> Token:
        user = await self.user_repository.get_user_by_email(email=schema.email)
        if not user:
            raise UnauthorizedException
        if not security.verify_password(password=schema.password, hashed_password=user.password):
            raise UnauthorizedException
        return self.get_token(
            user_id=user.id
        )

    @staticmethod
    def get_token(user_id: int) -> Token:
        access_token = security.create_access_token(identity=user_id)
        refresh_token = security.create_refresh_token(identity=user_id)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    async def refresh_token(self, user_id: int) -> Token:
        return self.get_token(user_id=user_id)