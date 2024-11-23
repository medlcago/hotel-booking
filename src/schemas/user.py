from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field

from schemas.pagination import PaginationParams


class UserParams(PaginationParams):
    limit: Annotated[int, Field(ge=1, le=100)] = 100
    is_active: bool | None = None
    is_verified: bool | None = None
    is_admin: bool | None = None


class UserResponse(BaseModel):
    full_name: str
    email: str
    phone: str | None = None
    date_of_birth: date | None = None
    loyalty_points: int
    is_active: bool
    is_verified: bool
    is_admin: bool
