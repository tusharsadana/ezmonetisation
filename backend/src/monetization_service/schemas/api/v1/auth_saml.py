# thirdparty
from pydantic import Field

# project
from src.common.schemas.base import BaseModel


class UserSchema(BaseModel):
    """Schema for SAML user"""

    first_name: str | None = Field(title="user first name")
    last_name: str | None = Field(title="user last name")
    email: str = Field(title="user email")
