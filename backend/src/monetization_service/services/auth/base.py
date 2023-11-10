# stdlib
import datetime
import logging

# thirdparty
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from redis.exceptions import ConnectionError

# project
from src.monetization_service.core.redis import Redis, get_redis_client
from src.monetization_service.schemas.api.v1.auth import Token
from src.monetization_service.schemas.common_enums import PERMISSIONS_PER_ROLE
from src.monetization_service.services.auth.jwt import (
    JWTService,
    get_jwt_service,
)
from src.monetization_service.settings.development import settings

logger = logging.getLogger(__name__)


class BaseAuth:
    def __init__(
        self,
        jwt_service: JWTService = get_jwt_service(),
        redis_client: Redis = get_redis_client(),
    ):
        self.jwt = jwt_service
        self.redis = redis_client

    async def delete_secret(self, email: str):
        await self.redis.delete(email)

    async def get_jwt_secret_key(self, email: str) -> str:
        """Get JWT secret key from Redis"""
        try:
            jwt_secret_key = await self.redis.get(email)
        except ConnectionError as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redis connection error",
            )
        return jwt_secret_key

    async def logged_out_tokens(self, *tokens: tuple[Token, str]):
        """Adding not expired tokens after refresh/logout to avoid reusing"""
        pipe = await self.redis.pipeline()
        for decoded, encoded in tokens:
            # if token is not already expired put it in redis
            if decoded.expiration > (
                now := datetime.datetime.now(tz=datetime.timezone.utc)
            ):
                ex = (decoded.expiration - now).seconds
                if ex > 0:
                    pipe.set(value=decoded.email, name=encoded, ex=ex)
                    pipe.set(
                        value=datetime.datetime.now(
                            tz=datetime.timezone.utc
                        ).strftime("%m/%d/%Y, %H:%M:%S"),
                        name=encoded + ":time",
                        ex=ex,
                    )
        await pipe.execute()

    async def generate_token_pair(
        self, email: str, **kwargs
    ) -> tuple[str, str]:
        """Generates access and refresh token pair"""

        jwt_secret_key_for_user = await self.get_jwt_secret_key(email)

        if jwt_secret_key_for_user is None:
            jwt_secret_key_for_user = self.jwt.generate_secret_key()

        await self.redis.set(
            email, jwt_secret_key_for_user, ex=settings.jwt_refresh_lifetime
        )

        access = self.jwt.generate_token(
            email=email,
            jwt_secret_key=jwt_secret_key_for_user,
            lifetime=settings.jwt_access_lifetime,
            **kwargs,
        )
        refresh = self.jwt.generate_token(
            email=email,
            jwt_secret_key=jwt_secret_key_for_user,
            lifetime=settings.jwt_refresh_lifetime,
            **kwargs,
        )

        return access, refresh

    async def decode_tokens(
        self,
        access_token: str,
        refresh_token: str,
        access_verify: bool,
        refresh_verify: bool,
        jwt_secret_key: str,
    ) -> tuple[Token, Token]:
        """
        Decode expired tokens
        """

        access = self.jwt.decode(
            access_token,
            jwt_secret_key=jwt_secret_key,
            options={"verify_exp": access_verify},
        )
        refresh = self.jwt.decode(
            refresh_token,
            jwt_secret_key=jwt_secret_key,
            options={"verify_exp": refresh_verify},
        )

        return access, refresh

    async def validate_token(
        self, token: str, jwt_secret_key: str
    ) -> tuple[bool, Token | None]:
        """Token validation"""
        # logger.info("Token validation")
        try:
            payload = self.jwt.decode(
                token=token, jwt_secret_key=jwt_secret_key
            )
        except (InvalidTokenError, ExpiredSignatureError, TypeError) as e:
            logging.error(e)
            return False, None
        else:
            # check if someone is trying to reuse withdrawn token
            try:
                withdrawn = await self.redis.get(token)
                time_of_set = await self.redis.get(token + ":time")
            except ConnectionError:
                self.redis = get_redis_client()
                withdrawn = await self.redis.get(token)
                time_of_set = await self.redis.get(token + ":time")

            if withdrawn is not None:
                if time_of_set is None:
                    return False, payload
                else:
                    # let use expired token for 5 seconds after setup to redis for handle concurrency from frontend
                    time_of_set = datetime.datetime.strptime(
                        time_of_set,
                        "%m/%d/%Y, %H:%M:%S",
                    ).replace(tzinfo=datetime.timezone.utc)
                    if (
                        datetime.datetime.now(tz=datetime.timezone.utc)
                        - time_of_set
                    ).seconds > 5:
                        return False, payload

            return True, payload

    async def refresh_token(
        self, access_token, refresh_token
    ) -> tuple[str, str]:
        """Tokens refresh"""
        email = self.jwt.extract_email_from_token(refresh_token)

        if email:
            jwt_secret_key = await self.get_jwt_secret_key(email)
            validated, payload = await self.validate_token(
                token=refresh_token, jwt_secret_key=jwt_secret_key
            )
        else:
            validated = None

        # user can't refresh token with invalid previous one
        if not validated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # put unexpired tokens to redis
        access_decoded, refresh_decoded = await self.decode_tokens(
            access_token=access_token,
            refresh_token=refresh_token,
            access_verify=False,
            refresh_verify=False,
            jwt_secret_key=jwt_secret_key,
        )

        access, refresh = await self.generate_token_pair(
            email=refresh_decoded.email,
            role=refresh_decoded.role,
            permissions=PERMISSIONS_PER_ROLE[refresh_decoded.role],
        )
        # putting in redis
        if access != access_token:
            # handle case when you do in the same second
            await self.logged_out_tokens(
                (access_decoded, access_token),
                (refresh_decoded, refresh_token),
            )

        return access, refresh
