from dataclasses import dataclass

from core import security
from core.exceptions import (
    UserAlreadyExists,
    BadCredentials,
    UserInactive,
    TokenExpired,
    UserAlreadyVerified,
)
from repositories.user import IUserRepository
from schemas.auth import SignInRequest
from schemas.auth import SignUpRequest
from schemas.response import Message
from schemas.token import Token
from schemas.user import UserResponse
from tasks import send_confirmation_email


@dataclass(frozen=True, slots=True)
class AuthService:
    user_repository: IUserRepository

    async def sign_up(self, schema: SignUpRequest) -> UserResponse:
        user = await self.user_repository.get_user_by_email(email=schema.email)
        if user:
            raise UserAlreadyExists

        schema.password = security.hash_password(schema.password)
        user = await self.user_repository.create_user(values=schema.model_dump())
        token = security.create_url_safe_token(data=dict(email=schema.email, action="verify_email"))
        send_confirmation_email.delay(email=schema.email, token=token)
        return UserResponse.model_validate(user, from_attributes=True)

    async def sign_in(self, schema: SignInRequest) -> Token:
        user = await self.user_repository.get_user_by_email(email=schema.email)
        if not user:
            raise BadCredentials
        if not security.verify_password(password=schema.password, hashed_password=user.password):
            raise BadCredentials
        if not user.is_active:
            raise UserInactive
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

    async def verify_email(self, token: str) -> Message:
        payload = security.decode_url_safe_token(token=token, max_age=86400)
        if not payload:
            raise TokenExpired
        email, action = payload.get("email"), payload.get("action")
        if not email or action != "verify_email":
            raise TokenExpired
        user = await self.user_repository.get_user_by_email(email=email)
        if not user or user.is_verified:
            raise TokenExpired
        await self.user_repository.update_user(user_id=user.id, values=dict(is_verified=True))
        return Message(
            message="E-mail successfully verified!"
        )

    async def send_confirmation_email(self, email: str) -> Message:
        user = await self.user_repository.get_user_by_email(email=email)
        if not user:
            raise BadCredentials
        if user.is_verified:
            raise UserAlreadyVerified
        token = security.create_url_safe_token(data=dict(email=email, action="verify_email"))
        send_confirmation_email.delay(email=email, token=token)
        return Message(
            message="E-mail successfully sent!"
        )
