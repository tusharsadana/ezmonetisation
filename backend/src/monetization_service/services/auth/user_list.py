# stdlib
import logging
import random
import string

# thirdparty
import secrets
import smtplib
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# project
from src.common.utils import SingletonWithArgs
from src.monetization_service.core.db import get_session_cm
from src.monetization_service.models.user import User
from src.monetization_service.queries.users import (
    update_user_password, add_new_user_query, user_isactive, get_verification_token, add_verification_token,
    token_isvalid, activate_user, delete_user
)
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

    async def drop_token(self, user_email: str):
        await self.delete_secret(user_email)

    async def reset_password(
        self, user_email: str, length: int = 10
    ) -> (bool, str | None):
        new_password = self.__generate_new_password(length=length)
        async with get_session_cm() as session:
            session: AsyncSession
            query = update_user_password(user_email, new_password)
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
    ):
        async with get_session_cm() as session:
            session: AsyncSession
            query = add_new_user_query(user_data.user_email, user_data.password, 1, user_data.first_name,
                                       user_data.last_name)
            try:
                await session.execute(query)
            except IntegrityError:
                return False, "Account with given user_email already exists"
            await session.commit()
            return True, None

    async def generate_random_token(self, user_email):
        async with get_session_cm() as session:
            session: AsyncSession
            query = user_isactive(user_email)
            result = await session.execute(query)
            result = result.all()
            if len(result):
                if result[0][0]:
                    return None, "Account is already active"
            else:
                return None, "Invalid user_email"
            query = get_verification_token(user_email)
            result = await session.execute(query)
            result = result.all()
            if len(result):
                random_token = result[0][0]
            else:
                random_token = secrets.token_hex(32)
            repeated_token = True
            while repeated_token:
                query = token_isvalid(random_token)
                result = await session.execute(query)
                result = result.all()
                if len(result):
                    random_token = secrets.token_hex(32)
                else:
                    repeated_token = False
            query = add_verification_token(user_email, random_token)
            await session.execute(query)
            await session.commit()

            return random_token, None

    async def send_email(
        self, user_email: str, link: str
    ):
        sender_email = "verifyuremail2023@gmail.com"
        receiver_email = user_email
        subject = "EzMonetization: Verify your email"
        body = f"Open the link to verify your account. {link}"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        smtp_server = "smtp.gmail.com"
        port = 587
        password = "fhkr sovv rjuz ufnk"

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()

            server.login(sender_email, password)
            try:
                server.sendmail(sender_email, receiver_email, message.as_string())

            except smtplib.SMTPRecipientsRefused:
                async with get_session_cm() as session:
                    session: AsyncSession
                    user_query, verification_token_query = delete_user(user_email)
                    await session.execute(verification_token_query)
                    await session.execute(user_query)
                    await session.commit()
                return False, "Invalid email. Please sign up using a different email"

        return True, None



    async def verify_user(
        self, token: str
    ):
        async with get_session_cm() as session:
            session: AsyncSession
            query = token_isvalid(token)
            result = await session.execute(query)
            result = result.all()
            if len(result):
                user_email = result[0][0]
            else:
                return False, "Invalid verification link"

            query = activate_user(user_email)
            await session.execute(query)
            await session.commit()

            return True, "Your email has been verified"






