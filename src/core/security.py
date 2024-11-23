from datetime import datetime, UTC, timedelta
from typing import Any

import bcrypt
import jwt
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import SecretStr

from core.exceptions import UnauthorizedException
from core.settings import settings
from enums.token import TokenType


def _get_secret(secret: str | SecretStr) -> str:
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
DEFAULT_TOKEN_LIFETIME = timedelta(minutes=10)


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
        claims: dict[str, Any] = None,
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


def create_access_token(identity: int, claims: dict[str, Any] = None) -> str:
    return create_token(
        identity=identity,
        token_type=TokenType.access,
        claims=claims,
        lifetime=settings.access_token_lifetime
    )


def create_refresh_token(identity: int, claims: dict[str, Any] = None) -> str:
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


def get_identity(token: str, token_type: TokenType | None = None) -> int | None:
    payload = decode_token(token=token)
    if not (payload and payload.get("identity")):
        return
    if token_type and payload.get("token_type") != token_type:
        return
    return payload.get("identity")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, token_type: TokenType = TokenType.access):
        super().__init__(auto_error=auto_error)
        self.token_type = token_type

    async def __call__(self, request: Request) -> int:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise UnauthorizedException
        identity = get_identity(token=credentials.credentials, token_type=self.token_type)
        if not identity:
            raise UnauthorizedException
        return identity
