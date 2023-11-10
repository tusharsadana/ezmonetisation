# stdlib
from typing import Optional

# thirdparty
from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request

# project
from src.monetization_service.schemas.api.v1.auth import Token
from src.monetization_service.services.auth.base import BaseAuth
from src.monetization_service.services.auth.saml import SamlAuth
from src.monetization_service.services.auth.user_list import UserListAuth


class ApiKeyHeaderPatched(APIKeyHeader):
    # FastAPI return incorrect status, small patch of this function
    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                )
            else:
                return None
        return api_key


api_key = ApiKeyHeaderPatched(name="Authorization")


async def get_user_list_auth() -> UserListAuth:
    return UserListAuth()


def get_saml_auth() -> SamlAuth:
    return SamlAuth()


async def get_auth_service() -> BaseAuth:
    return await get_user_list_auth()


class Authenticated:
    async def __call__(
        self,
        service: BaseAuth = Depends(get_auth_service),
        token: str = Security(api_key),
    ) -> tuple[bool, Token]:
        """
        Authorization routine
        """
        email = service.jwt.extract_email_from_token(token)
        validated = False

        if email:
            jwt_secret_key = await service.get_jwt_secret_key(email)

            if jwt_secret_key:
                # token validation
                validated, payload = await service.validate_token(
                    token, jwt_secret_key
                )

        # if token is expired or invalid raise 401
        if not validated:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return validated, payload


class Authorized(Authenticated):
    """Dependency for endpoints that require authorization"""

    def __init__(self, *roles: int):
        self.roles = roles

    async def __call__(
        self,
        service: BaseAuth = Depends(get_auth_service),
        token: str = Security(api_key),
    ):
        """
        Authorization routine
        """

        # token validation
        validated, payload = await super(Authorized, self).__call__(
            service=service, token=token
        )
        # logging.info("Authorization")
        # if user role is not in allowed roles list raise 403
        if payload.user_type in self.roles:
            return validated, payload
        else:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Don't have enough permissions",
            )
