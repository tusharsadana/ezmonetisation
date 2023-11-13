# thirdparty
from sqlalchemy import Insert, Update, insert, update, select

# project
from src.monetization_service.models.user import User


def user_exists(username: str):
    query = select(User).where(User.email == username)
    return query


def update_user_password(username: str, password: str) -> Update:
    query = (
        update(User)
        .values({"password": password})
        .where(User.is_active.is_(True), User.email == username)
    )

    return query


def add_new_user_query(username: str, password: str, user_type: int, first_name: str, last_name: str) -> Insert:
    query = insert(User).values(
        {"email": username, "password": password, "user_type": user_type, "first_name": first_name, "last_name": last_name}
    )

    return query
