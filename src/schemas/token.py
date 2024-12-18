from pydantic import BaseModel

from enums.token import TokenType


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class Token(AccessToken, RefreshToken):
    token_type: str = "Bearer"


class TokenResult(BaseModel):
    token: str
    token_type: TokenType
    user_id: int
