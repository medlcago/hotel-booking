from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=64)]
    last_name: Annotated[str, Field(min_length=2, max_length=64)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=60)]


class SignInRequest(BaseModel):
    email: EmailStr
    password: str
