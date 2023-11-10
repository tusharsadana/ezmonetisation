# stdlib
import io
import logging
import tempfile
from contextlib import contextmanager
from typing import BinaryIO, Iterator, Union

# thirdparty
import boto3
from botocore.exceptions import ClientError

# project
from src.common.file_storage.base import BaseFileStorage

logger = logging.getLogger(__name__)


class S3Storage(BaseFileStorage):
    """
    Class for working with AWS S3
    for deployment=instance
    """

    def __init__(
        self,
        bucket_name: str,
    ):
        self.bucket_name = bucket_name
        self.session = boto3.session.Session()

        self.s3_client = self.session.client("s3")

    def upload(
        self, file: tempfile.SpooledTemporaryFile, file_name: str
    ) -> bool:
        """upload file to s3 bucket"""

        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, file_name)
        except ClientError as e:
            logger.error(
                "Error during file uploading, file_name = %s" % file_name
            )
            logger.error(e)
            return False

        return True

    @contextmanager
    def get_file(self, file_name) -> BinaryIO:
        try:
            a = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=file_name
            )["Body"]
        except ClientError as e:
            logger.exception(e)
            raise e
        else:
            yield io.BufferedReader(a._raw_stream)

    def is_file_exists(self, file_name: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_name)
        except ClientError:
            return False
        else:
            return True

    def download(
        self, file_name: str, return_iterator: bool = True
    ) -> Union[Iterator[bytes], bytes, None]:

        """download file from s3 bucket"""

        try:
            file = self.s3_client.get_object(
                Bucket=self.bucket_name, Key=file_name
            )
            file_object = file["Body"]
        except ClientError as e:
            logger.error(
                "Error during file downloading, file_name = %s" % file_name
            )

            if e.response["Error"]["Code"] == "404":
                logger.error("File %s doesn't exist" % file_name)
            logger.error(e)
            return None

        if return_iterator:
            return file_object.iter_chunks()

        return file_object.read()

    def delete(self, file_name: str):
        """
        Delete file from local storage

        :param file_name: file name
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name, Key=file_name
            )
        except ClientError as e:
            logger.error(
                "Error during file deleting, file_name = %s" % file_name
            )
            logger.exception(e)


class S3StorageK8S(S3Storage):
    """
    Class for working with AWS S3
    for deployment=k8s
    """

    def __init__(
        self,
        bucket_name: str,
        aws_session_role_duration,
        aws_session_name,
        aws_iam_role,
        aws_region,
        aws_identity_token_file,
    ):
        super().__init__(
            bucket_name,
        )
        self.sts_client = self.session.client("sts")
        self.aws_identity_token_file = aws_identity_token_file
        self.aws_session_role_duration = aws_session_role_duration
        self.aws_session_name = aws_session_name
        self.aws_iam_role = aws_iam_role
        self.aws_region = aws_region

        self._s3_client_with_role()

    def upload(
        self, file: tempfile.SpooledTemporaryFile, file_name: str
    ) -> bool:
        """upload file to s3 bucket"""
        self._s3_client_with_role()
        return super().upload(file, file_name)

    def delete(self, file_name: str):
        self._s3_client_with_role()
        return super().delete(file_name)

    def get_file(self, file_name) -> BinaryIO:
        self._s3_client_with_role()
        return super().get_file(file_name)

    def download(
        self, file_name: str, return_iterator: bool = True
    ) -> Union[Iterator[bytes], bytes, None]:
        self._s3_client_with_role()
        return super().download(file_name, return_iterator)

    def _get_web_token(self):
        """Get web token for AWS S3"""
        with open(self.aws_identity_token_file, "r") as content_file:
            token = content_file.read()
        return token

    def _s3_client_with_role(self):
        """Assume role for AWS S3 and return new client"""
        logger.info("Refreshing s3 token")
        web_identity_token = self._get_web_token()
        if web_identity_token:
            try:
                role = self.sts_client.assume_role_with_web_identity(
                    RoleArn=self.aws_iam_role,
                    RoleSessionName=self.aws_session_name,
                    DurationSeconds=self.aws_session_role_duration,
                    WebIdentityToken=web_identity_token,
                )
            except Exception as e:
                logger.info(e)
                raise e
        else:
            raise ValueError("Web identity token is empty")

        self.s3_client = self.session.client(
            "s3",
            region_name=self.aws_region,
            aws_access_key_id=role["Credentials"]["AccessKeyId"],
            aws_secret_access_key=role["Credentials"]["SecretAccessKey"],
            aws_session_token=role["Credentials"]["SessionToken"],
        )
        logger.info("s3 token successfully refreshed")
