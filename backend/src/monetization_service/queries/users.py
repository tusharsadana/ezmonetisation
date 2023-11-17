# thirdparty
from sqlalchemy import Insert, Update, insert, update, select, and_

# project
from src.monetization_service.models.user import User, UserTypeConstants


def user_exists(user_email: str):
    query = select(User).where(and_(User.email == user_email, User.is_active))
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
        {"email": user_email, "password": password, "user_type": user_type, "first_name": first_name, "last_name": last_name}
    )

    return query


def user_ratio(user_email: str):
    query = (
        select(UserTypeConstants.watch_hour_ratio, UserTypeConstants.subscriber_ratio)
        .join(User, User.user_type == UserTypeConstants.user_type_id)
        .where(User.email == user_email)
    )
    return query


def user_num(user_email: str):
    query = (
        select(UserTypeConstants.fetch_video, UserTypeConstants.fetch_channel)
        .join(User, User.user_type == UserTypeConstants.user_type_id)
        .where(User.email == user_email)
    )
    return query
