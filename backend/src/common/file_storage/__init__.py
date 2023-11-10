# stdlib
from functools import lru_cache

# project
from src.common.constants import DeploymentType
from src.common.file_storage.base import BaseFileStorage
from src.common.file_storage.local import LocalStorage
from src.common.file_storage.s3 import S3Storage, S3StorageK8S


@lru_cache
def get_storage(
    storage_type: str,
    docs_path: str,
    s3_bucket: str,
    deployment_type: DeploymentType,
    aws_session_role_duration,
    aws_session_name,
    aws_iam_role,
    aws_region,
    aws_identity_token_file,
) -> BaseFileStorage:
    """Get instance of FileStorage for DI"""
    if storage_type == "s3":
        if deployment_type == DeploymentType.k8s:
            return S3StorageK8S(
                s3_bucket,
                aws_session_role_duration,
                aws_session_name,
                aws_iam_role,
                aws_region,
                aws_identity_token_file,
            )
        else:
            return S3Storage(
                s3_bucket,
            )
    else:
        return LocalStorage(docs_path)
