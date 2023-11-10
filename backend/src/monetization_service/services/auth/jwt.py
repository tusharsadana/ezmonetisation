# stdlib
import functools
import secrets
from datetime import datetime, timedelta, timezone

# thirdparty
import jwt

# project
from src.monetization_service.schemas.api.v1.auth import Token
from src.monetization_service.settings.development import settings


class JWTService:
    @staticmethod
    def extract_email_from_token(access_token: str) -> str | None:
        """Extracts email from token"""
        try:
            decoded_token = jwt.decode(
                access_token, options={"verify_signature": False}
            )
        except jwt.exceptions.DecodeError:
            return None
        return decoded_token.get("Email ID")

    @staticmethod
    def generate_secret_key() -> str:
        return secrets.token_hex(32)

    @staticmethod
    def generate_token(lifetime: int, jwt_secret_key: str, **kwargs) -> str:
        """Generates token"""
        claims = Token(
            expiration=(
                datetime.now(tz=timezone.utc) + timedelta(seconds=lifetime)
            ).timestamp(),
            **kwargs
        )

        token = jwt.encode(
            payload=claims.dict(by_alias=True),
            algorithm=settings.jwt_algorithm,
            key=jwt_secret_key,
        )

        return token

    @staticmethod
    def decode(token: str, jwt_secret_key: str, **kwargs) -> Token:
        """Decodes token"""
        decoded = jwt.decode(
            jwt=token,
            key=jwt_secret_key,
            algorithms=settings.jwt_algorithm,
            **kwargs
        )

        return Token.parse_obj(decoded)


@functools.cache
def get_jwt_service():
    return JWTService()
