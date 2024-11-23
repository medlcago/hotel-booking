from datetime import date

from pydantic import BaseModel


class UserResponse(BaseModel):
    full_name: str
    email: str
    phone: str | None = None
    date_of_birth: date | None = None
    loyalty_points: int
    is_active: bool
    is_verified: bool
    is_admin: bool
