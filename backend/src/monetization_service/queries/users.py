# thirdparty
from sqlalchemy import Insert, Update, insert, update

# project
from src.monetization_service.models.user import User


def update_user_password(username: str, password: str) -> Update:
    query = (
        update(User)
        .values({"password": password})
        .where(User.is_active.is_(True), User.email == username)
    )

    return query


def add_new_user_query(username: str, password: str, role: str, first_name: str, last_name: str) -> Insert:
    query = insert(User).values(
        {"email": username, "password": password, "role_name": role, "first_name": first_name, "last_name": last_name}
    )

    return query
