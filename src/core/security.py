import random
from datetime import datetime, UTC, timedelta
from typing import Any

import bcrypt
import jwt
from fastapi.requests import Request
from fastapi.security import HTTPBearer
from itsdangerous import URLSafeTimedSerializer, BadData
from pydantic import SecretStr

from core.exceptions import UnauthorizedException
from core.settings import settings
from enums.token import TokenType
from schemas.token import TokenResult


def _get_secret(secret: str | SecretStr) -> str:
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
DEFAULT_TOKEN_LIFETIME = timedelta(minutes=10)

serializer = URLSafeTimedSerializer(secret_key=_get_secret(SECRET_KEY))


def create_url_safe_token(data: dict[str, Any]) -> str:
    return serializer.dumps(data)


def decode_url_safe_token(token: str, max_age: int | None = None) -> dict[str, Any] | None:
    try:
        return serializer.loads(token, max_age=max_age)
    except BadData:
        return None


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(
        password=password.encode("utf-8"),
        salt=salt
    )
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8")
    )


def create_token(
        identity: int,
        token_type: TokenType,
        claims: dict[str, Any] | None = None,
        lifetime: timedelta = DEFAULT_TOKEN_LIFETIME
) -> str:
    payload = dict(
        identity=identity,
        iat=datetime.now(UTC),
        exp=datetime.now(UTC) + lifetime,
        token_type=token_type,
        **claims if claims else {}
    )

    token = jwt.encode(
        payload=payload,
        key=_get_secret(SECRET_KEY),
        algorithm=ALGORITHM,

    )
    return token


def create_access_token(identity: int, claims: dict[str, Any] | None = None) -> str:
    return create_token(
        identity=identity,
        token_type=TokenType.access,
        claims=claims,
        lifetime=settings.access_token_lifetime
    )


def create_refresh_token(identity: int, claims: dict[str, Any] | None = None) -> str:
    return create_token(
        identity=identity,
        token_type=TokenType.refresh,
        claims=claims,
        lifetime=settings.refresh_token_lifetime
    )


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            jwt=token,
            key=_get_secret(SECRET_KEY),
            algorithms=[ALGORITHM],
        )
        return payload
    except jwt.PyJWTError:
        return {}


def generate_code() -> str:
    return str(random.randint(100000, 999999))


class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> TokenResult:
        credentials = await super().__call__(request)
        if not credentials:
            raise UnauthorizedException("Invalid credentials")
        token_data = decode_token(token=credentials.credentials)
        if not token_data:
            raise UnauthorizedException("Invalid token")
        self.verify_token_data(token_data)
        user_id = self.get_user_id(token_data=token_data)
        return TokenResult(
            token=credentials.credentials,
            token_type=token_data.get("token_type"),
            user_id=user_id
        )

    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        raise NotImplementedError

    @staticmethod
    def get_user_id(token_data: dict[str, Any]) -> int:
        user_id = token_data.get("identity")
        if not user_id:
            raise UnauthorizedException("Invalid token")
        return user_id


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if token_data.get("token_type") != TokenType.access:
            raise UnauthorizedException("Invalid token type")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if token_data.get("token_type") != TokenType.refresh:
            raise UnauthorizedException("Invalid token type")
