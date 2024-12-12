# thirdparty
from sqlalchemy import Insert, Update, insert, update, select, and_, Delete
from sqlalchemy.sql.functions import func
# project
from src.monetization_service.models.user import User, UserTypeConstants as utc, VerificationToken


def user_exists(user_email: str):
    query = select(User.first_name, User.last_name).where(and_(User.email == user_email, User.is_active))
    return query


def user_isactive(user_email: str):
    query = select(User.is_active).where(User.email == user_email)
    return query


def add_verification_token(user_email: str, token: str) -> Insert:
    query = insert(VerificationToken).values(
        {"user_email": user_email, "token": token}
    )

    return query


def get_verification_token(user_email: str):
    query = select(VerificationToken.token).where(VerificationToken.user_email == user_email)
    return query


def update_user_password(user_email: str, password: str) -> Update:
    query = (
        update(User)
        .values({"password": password})
        .where(User.is_active.is_(True), User.email == user_email)
    )

    return query


def add_new_user_query(user_email: str, password: str, user_type: int, first_name: str, last_name: str) -> Insert:
    query = insert(User).values(
        {"email": user_email, "password": password, "user_type": user_type, "first_name": first_name,
         "last_name": last_name, "is_active": False}
    )

    return query


def user_ratio(user_email: str):
    query = (
        select(utc.watch_hour_ratio, utc.subscriber_ratio)
        .join(User, User.user_type == utc.user_type_id)
        .where(User.email == user_email)
    )
    return query


def user_num_limit(user_email: str):
    query = (
        select(utc.fetch_video, utc.fetch_channel)
        .join(User, User.user_type == utc.user_type_id)
        .where(User.email == user_email)
    )
    return query


def activate_user(user_email: str):
    query = (
        update(User)
        .values({"is_active": True})
        .where(User.email == user_email)
    )
    return query


def token_isvalid(token: str):
    query = (
        select(VerificationToken.user_email)
        .where(VerificationToken.token == token)
    )
    return query


def delete_user(user_email: str):
    user_query = (
        Delete(User)
        .where(User.email == user_email)
    )
    verification_token_query = (
        Delete(VerificationToken)
        .where(VerificationToken.user_email == user_email)
    )
    return user_query, verification_token_query


def user_watch_privileges(user_email: str):
    query = (
        select(
            func.json_agg(
                func.json_build_object(
                    'user_type', utc.user_type_name,
                    'maximum_video_duration', utc.max_video_duration,
                    'watch_hours_ratio', utc.watch_hour_ratio,
                    'allowed_fetch_videos', utc.fetch_video,
                    'minimum_videos_allowed', utc.min_videos_allowed,
                    'maximum_videos_allowed', utc.max_videos_allowed,
                )
            ).label('privileges')
        )
        .join(User, User.user_type == utc.user_type_id)
        .where(User.email == user_email)
    )
    return query


def user_subscriber_privileges(user_email: str):
    query = (
        select(
            func.json_agg(
                func.json_build_object(
                    'user_type', utc.user_type_name,
                    'subscriber_ratio', utc.subscriber_ratio,
                    'allowed_fetch_channel', utc.fetch_channel,
                )
            ).label('privileges')
        )
        .join(User, User.user_type == utc.user_type_id)
        .where(User.email == user_email)
    )
    return query
