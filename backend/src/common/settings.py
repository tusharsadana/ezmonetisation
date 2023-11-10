# stdlib
import os
import pathlib
from typing import Union

# thirdparty
from dotenv import find_dotenv
from pydantic import BaseSettings, Field

# project
from src.common.constants import DeploymentType, ServiceName, StorageType


class MqSettings(BaseSettings):
    """Message Queue Broker Settings"""

    mq_host: Union[str, None] = Field(env="MQ_HOST")
    mq_port: Union[str, None] = Field(env="MQ_PORT")
    mq_user: Union[str, None] = Field(env="MQ_USER")
    mq_password: Union[str, None] = Field(env="MQ_PASSWORD")


class AWSSettings(BaseSettings):
    session_role_duration: int = Field(
        title="life duration of role session",
        env="AWS_SESSION_ROLE_DURATION",
        default=3600,
    )
    iam_role: str = Field(
        title="iam role endpoint",
        env="AWS_IAM_ROLE",
        default="arn:aws:iam::139013895924:role/eks-to-s3-role",
    )
    session_name: str = Field(
        title="name of session",
        env="AWS_SESSION_NAME",
        default="zeros3session",
    )
    region: str = Field(
        title="aws region", env="AWS_REGION", default="eu-west-1"
    )
    identity_token_file: str = Field(
        title="aws identity",
        env="AWS_IDENTITY",
        default="/var/run/secrets/eks.amazonaws.com/serviceaccount/token",
    )
    instance_role_name: str = Field(
        title="Name of instance role",
        env="AWS_INSTANCE_ROLE_NAME",
        default="demo.artemis.zerocs.net",
    )
    token_url: str = Field(
        title="token endpoint url",
        env="AWS_TOKEN_URL",
        default="http://169.254.169.254/latest/api/token",
    )
    metadata_url: str = Field(
        title="metadata endpoint url",
        env="AWS_METADATA_ENDPOINT",
        default="http://169.254.169.254/latest/"
        "meta-data/iam/security-credentials/$INSTANCE_ROLE_NAME",
    )


class Settings(BaseSettings):
    storage_type: StorageType = Field(
        env="STORAGE_TYPE", default=StorageType.local, title="storage type"
    )
    s3_bucket_name: Union[str, None] = Field(
        env="BUCKET_NAME", title="s3 bucket name"
    )
    docs_path: Union[str, None] = Field(
        env="DOCS_PATH", title="path to root dir of saving docs"
    )
    deployment_type: DeploymentType = Field(
        env="DEPLOYMENT_TYPE",
        title="where it is deployed",
        default=DeploymentType.k8s,
    )
    project_dir = pathlib.Path(__file__).parents[1]

    aws_settings: AWSSettings = AWSSettings()


def settings_file_path_for_env(service: ServiceName) -> str:
    """get path to settings file"""
    current_env = os.environ.get("ENV", "dev")

    env_files_mapping = {
        "dev": ".env.dev.{}".format(service.value),
        "prod": ".env.prod.{}".format(service.value),
        "test": ".env.test.{}".format(service.value),
    }

    env_file_path = find_dotenv(env_files_mapping[current_env]) or None
    return env_file_path
