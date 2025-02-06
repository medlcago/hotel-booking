from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from utils.validators import PasswordStr


class SignUpRequest(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=64)]
    last_name: Annotated[str, Field(min_length=2, max_length=64)]
    email: EmailStr
    password: PasswordStr


class SignInRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class ConfirmEmailRequest(BaseModel):
    email: EmailStr
    code: str
