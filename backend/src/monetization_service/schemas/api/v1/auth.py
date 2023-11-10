# stdlib
import enum
from datetime import datetime

# thirdparty
from pydantic import EmailStr, Field

# project
from src.common.schemas.base import BaseModel


class TokenType(str, enum.Enum):
    refresh = "refresh"
    access = "access"


class AuthInput(BaseModel):
    username: str = Field(title="Email")
    password: str = Field(title="Password")


class ResetPassword(BaseModel):
    username: EmailStr = Field(title="Email")
    length: int = Field(title="length", ge=8, le=100, default=10)


class TokenClaims(BaseModel):
    email: str | None = Field(title="user email", alias="Email ID")
    user_type: int | None = Field(
        title="List of user roles", default=1
    )

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class UserSchema(TokenClaims):
    password: str | None = Field(title="User password", alias="Password")

    class Config:
        orm_mode = True


class Token(TokenClaims):
    expiration: datetime = Field(title="Token lifetime", alias="exp")


class TokenPair(BaseModel):
    access: str = Field(title="Access token")
    refresh: str = Field(title="Refresh token")


class UserSignUp(AuthInput):
    first_name: str = Field(title="First name")
    last_name: str = Field(title="Last name")
