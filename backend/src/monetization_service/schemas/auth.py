from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_sample = {
            "example": {
                "fullname": "String",
                "email": "string@string.com",
                "password": "string"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_sample = {
            "example": {
                "email": "string@string.com",
                "password": "string"
            }
        }
