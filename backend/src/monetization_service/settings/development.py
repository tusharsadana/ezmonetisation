# stdlib
from enum import Enum
from functools import cache
from typing import Union

# thirdparty
from pydantic import BaseSettings, Field

# project
from src.common.constants import ServiceName
from src.common.settings import AWSSettings
from src.common.settings import MqSettings as BaseMqSettings
from src.common.settings import Settings as BaseProjectSettings
from src.common.settings import settings_file_path_for_env


class MqSettings(BaseMqSettings):
    """MQ settings"""

    # extraction queues
    mq_task_exchange: Union[str, None] = Field(
        env="MQ_TASK_EXCHANGE", title="name of exchange for extraction task"
    )
    mq_task_queue: Union[str, None] = Field(
        env="MQ_TASK_QUEUE",
        title="name of tasks message queue for extraction task",
    )
    mq_result_queue: Union[str, None] = Field(
        env="MQ_RESULT_QUEUE",
        title="name of results message queue for extraction task",
    )
    mq_prefetch_count: Union[int, None] = Field(
        env="MQ_PREFETCH_COUNT",
        title="how many messages simultaneously consume "
        "from rabbit for extraction task",
    )

    # preprocessing queues
    mq_task_exchange_pp: Union[str, None] = Field(
        env="MQ_TASK_EXCHANGE_PP",
        title="name of exchange for preprocessing task",
    )
    mq_task_queue_pp: Union[str, None] = Field(
        env="MQ_TASK_QUEUE_PP",
        title="name of tasks message queue for preprocessing task",
    )
    mq_result_queue_pp: Union[str, None] = Field(
        env="MQ_RESULT_QUEUE_PP",
        title="name of results message queue for preprocessing task",
    )
    mq_prefetch_count_pp: Union[int, None] = Field(
        env="MQ_PREFETCH_COUNT_PP",
        title="how many messages simultaneously consume "
        "from rabbit for preprocessing task",
    )


class PostgresSettings(BaseSettings):
    connection_number: Union[int, None] = Field(
        default=20, env="POSTGRES_POOL_SIZE"
    )
    max_connections: int = Field(default=100, env="POSTGRES_MAX_CONN")
    host: Union[str, None] = Field(default="localhost", env="POSTGRES_HOST")
    port: Union[int, None] = Field(default=5432, env="POSTGRES_PORT")
    db: Union[str, None] = Field(default="monetization_db", env="POSTGRES_DB")
    user: Union[str, None] = Field(default="admin", env="POSTGRES_USER")
    password: Union[str, None] = Field(
        default="123456", env="POSTGRES_PASSWORD"
    )


class UvicornSettings(BaseSettings):
    workers: int = Field(default=1, env="UVICORN_WORKERS")


class AuthType(str, Enum):
    user_list = "user_list"
    okta = "okta"


class OktaSettings(BaseSettings):
    entity_id: str | None = Field(env="OKTA_ENTITY_ID")
    sso_url: str | None = Field(
        title="okta url for single sign on", env="OKTA_SSO_URL"
    )
    x509_cert: str | None = Field(title="okta x509 cert", env="OKTA_X509_CERT")
    callback_url: str | None = Field(
        title="okta callback url", env="OKTA_CALLBACK_URL"
    )
    frontend_redirect_url: str | None = Field(
        title="redirect url for frontend after auth",
        env="OKTA_FRONTEND_REDIRECT_URL",
    )
    user_manager_okta: str | None = Field(
        title="default user manager email for settings page",
        env="USER_MANAGER_OKTA",
    )


class Settings(BaseProjectSettings):
    """Project settings"""

    # postgres settings
    db = PostgresSettings()

    # mq settings
    mq = MqSettings()
    release_version: str | None = Field(env="ARTEMIS_VERSION")

    # aws settings
    aws = AWSSettings()

    # okta settings
    okta = OktaSettings()

    # uvicorn settings
    uvicorn = UvicornSettings()

    # redis settings
    redis_host: str | None = Field(env="REDIS_HOST")
    redis_port: int | None = Field(env="REDIS_PORT")
    cache_expire: int | None = Field(
        env="CACHE_EXPIRE",
        title="how many seconds redis cache would exist",
        default=300,
    )
    redis_suggestions_idx_name: str | None = Field(
        env="REDIS_SUGGESTIONS_IDX_NAME",
        title="name of RediSearch index for suggestions",
        default="idx:suggestion",
    )
    redis_suggestions_prefix: str | None = Field(
        env="REDIS_SUGGESTIONS_PREFIX",
        title="name of RediSearch index for suggestions",
        default="suggestion",
    )
    jwt_access_lifetime: int = Field(
        title="access token lifetime, min",
        default=900,
        env="JWT_ACCESS_LIFETIME",
    )
    jwt_refresh_lifetime: int = Field(
        title="refresh token lifetime, min",
        default=14400,
        env="JWT_REFRESH_LIFETIME",
    )
    jwt_algorithm: str = Field(
        title="JWT encoding algorithm", default="HS256", env="JWT_ALGORITHM"
    )


@cache
def get_settings() -> Settings:
    """get current project settings"""

    env_file_path = settings_file_path_for_env(ServiceName.monetization)

    db = PostgresSettings(_env_file=env_file_path)
    mq = MqSettings(_env_file=env_file_path)
    aws = AWSSettings(_env_file=env_file_path)
    okta = OktaSettings(_env_file=env_file_path)
    return Settings(_env_file=env_file_path, db=db, mq=mq, aws=aws, okta=okta)


settings: Settings = get_settings()


@cache
def get_mq_conn_string():
    """get connection string of mq broker"""
    return (
        f"amqp://{settings.mq.mq_user}:{settings.mq.mq_password}"
        f"@{settings.mq.mq_host}:{settings.mq.mq_port}//"
    )
