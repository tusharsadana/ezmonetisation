# stdlib
import logging

# thirdparty
from fastapi import APIRouter, Depends, HTTPException, Response, status
from jwt import InvalidSignatureError

# project
from src.monetization_service.schemas.api.v1.auth import (
    AuthInput,
    ResetPassword,
    TokenPair,
    UserSchema,
    UserSignUp
)
from src.monetization_service.services.auth import SamlAuth, UserListAuth
from src.monetization_service.services.auth.utils import (
    Authorized,
    get_auth_service,
    get_user_list_auth,
)
from fastapi.responses import ORJSONResponse, Response

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@auth_router.post(
    path="/sign-up",
    description="Sign up user",
)
async def sign_up(
    auth_input: UserSignUp,
    auth_service: UserListAuth = Depends(get_user_list_auth),
):
    is_created = await auth_service.new_user(auth_input)
    if is_created:
        return ORJSONResponse(content={"description": "New account created successfully"},
                              status_code=status.HTTP_200_OK)
    return ORJSONResponse(content={"description": "Account with the given user_email already exists"},
                          status_code=status.HTTP_400_BAD_REQUEST)


@auth_router.post(
    path="/sign-in",
    description="Sign user in",
    response_model=TokenPair,
    responses={
        status.HTTP_200_OK: {"description": "User authenticated"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Wrong credentials"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request. "
            "Cause of status will be provided inside the body"
        },
    },
)
async def sign_in(
    auth_input: AuthInput,
    auth_service: UserListAuth = Depends(get_user_list_auth),
):
    """
    Endpoint for sign in

    Request body:
    **user_email** - UserEmail
    **password** - Password

    Current mapping of roles:
    """
    check, results = await auth_service.login(
        email=auth_input.user_email, password=auth_input.password
    )
    if not check:
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Wrong credentials",
        )

    results: UserSchema
    access, refresh = await auth_service.generate_token_pair(
        email=results.email,
        role=results.user_type,
    )

    return TokenPair(access=access, refresh=refresh)


@auth_router.post(
    path="/sign-out",
    description="Sign user out",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User has been already signed out"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request. Cause of status "
            "will be provided inside the body"
        },
        status.HTTP_200_OK: {"description": "Successfully logged out"},
    },
)
async def sign_out(
    token_pair: TokenPair,
    auth_service: UserListAuth | SamlAuth = Depends(get_auth_service),
):
    """
    Endpoint for sign out.

    Header has to be generated according to the following format:
    **Authorization: Bearer {access_token} Refresh {refresh token}**
    """
    email = auth_service.jwt.extract_email_from_token(token_pair.access)

    if email:
        jwt_secret_key = await auth_service.get_jwt_secret_key(email)

        if not jwt_secret_key:
            jwt_secret_key = auth_service.jwt.generate_secret_key()

        try:
            access_decoded, refresh_decoded = await auth_service.decode_tokens(
                access_token=token_pair.access,
                refresh_token=token_pair.refresh,
                access_verify=False,
                refresh_verify=False,
                jwt_secret_key=jwt_secret_key,
            )
            await auth_service.logged_out_tokens(
                (access_decoded, token_pair.access),
                (refresh_decoded, token_pair.refresh),
            )

        except InvalidSignatureError:
            logger.info("Invalid signature error for logout")

    return {"message": "Successfully logged out"}


@auth_router.post(
    path="/refresh",
    description="Refresh tokens",
    response_model=TokenPair,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token(s)"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request. Cause of status "
            "will be provided inside the body"
        },
        status.HTTP_200_OK: {"description": "Tokens had been refreshed"},
    },
)
async def refresh_tokens(
    token_pair: TokenPair,
    auth_service: UserListAuth = Depends(get_auth_service),
):
    """
    Endpoint for tokens refreshing.

    Header has to be generated according to the following format:
    **Authorization: Bearer {access_token} Refresh {refresh token}**
    """
    access, refresh = await auth_service.refresh_token(
        access_token=token_pair.access, refresh_token=token_pair.refresh
    )

    return TokenPair(access=access, refresh=refresh)


@auth_router.post(
    "/reset-password", dependencies=[Depends(Authorized(0))]
)
async def reset_password(
    payload: ResetPassword,
    auth_service: UserListAuth = Depends(get_user_list_auth),
):
    is_reset, new_password = await auth_service.reset_password(
        payload.user_email, payload.length
    )
    if is_reset:
        await auth_service.drop_token(payload.user_email)
        return {"new-password": new_password}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
