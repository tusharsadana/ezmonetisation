# stdlib
import logging
import random
import string

# thirdparty
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.common.utils import SingletonWithArgs
from src.monetization_service.core.db import get_session_cm
from src.monetization_service.models.user import User
from src.monetization_service.queries.users import update_user_password, add_new_user_query
from src.monetization_service.schemas.api.v1.auth import UserSchema, UserSignUp
from src.monetization_service.services.auth.base import BaseAuth


logger = logging.getLogger(__name__)


class UserListAuth(BaseAuth, metaclass=SingletonWithArgs):
    def __init__(self):
        super().__init__()

    async def check_user(
        self, email: EmailStr | str, password: str
    ) -> tuple[bool, UserSchema | None]:

        async with get_session_cm() as session:
            query = select(User).where(
                User.email == email, User.is_active.is_(True)
            )
            result = await session.execute(query)
            try:
                user = result.one()[0]
            except NoResultFound:
                return False, None
            is_auth = user.password == password
            if is_auth:
                return is_auth, UserSchema(
                    user_type=user.user_type, email=email, password=password
                )
            return False, None

    async def login(
        self, email: str, password: str
    ) -> tuple[bool, UserSchema | None]:
        """
        Downloads file with list with users and checks if the
        person is in it
        """
        check, results = await self.check_user(email=email, password=password)
        return check, results

    def __generate_new_password(self, length) -> str:
        new_password = random.choices(
            "".join(
                set(string.printable) - set(string.whitespace) - set("\\")
            ),
            k=length,
        )
        return "".join(new_password)

    async def drop_token(self, username: str):
        await self.delete_secret(username)

    async def reset_password(
        self, username: str, length: int = 10
    ) -> (bool, str | None):
        new_password = self.__generate_new_password(length=length)
        async with get_session_cm() as session:
            session: AsyncSession
            query = update_user_password(username, new_password)
            try:
                result = await session.execute(query)
            except IntegrityError:
                return False, None
            is_updated = result.rowcount == 1
            if is_updated:
                await session.commit()
                return True, new_password

            await session.rollback()
        return False, None

    async def new_user(
        self, user_data: UserSignUp
    ) -> bool:
        async with get_session_cm() as session:
            session: AsyncSession
            query = add_new_user_query(user_data.username, user_data.password, 1, user_data.first_name,
                                       user_data.last_name)
            try:
                result = await session.execute(query)
            except IntegrityError:
                return False
            is_created = result.rowcount == 1
            if is_created:
                await session.commit()
                return True

            await session.rollback()
        return False
