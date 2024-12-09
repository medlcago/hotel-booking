from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, EmailStr

from schemas.filters import LimitOffset
from utils.validators import PasswordType


class UserParams(LimitOffset):
    limit: Annotated[int, Field(ge=1, le=100)] = 100
    is_active: bool | None = None
    is_verified: bool | None = None
    is_admin: bool | None = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str | None = None
    date_of_birth: date | None = None
    loyalty_points: int
    is_active: bool
    is_verified: bool
    is_admin: bool


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: PasswordType
