# stdlib
import contextlib
import logging
import os
import tempfile
from typing import BinaryIO, Iterator, Union

# project
from src.common.file_storage.base import BaseFileStorage

logger = logging.getLogger(__name__)


class LocalStorage(BaseFileStorage):
    """Class for working with Local Storage"""

    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    def upload(
        self, file: tempfile.SpooledTemporaryFile, file_name: str
    ) -> bool:
        """
        upload file to local storage

        :param file_name: link to document
        :param file: file to upload

        """
        file_link = os.path.join(self.path, file_name)

        # check if folder for file exists
        folder_name = os.path.join(*os.path.split(file_name)[:-1])
        folder_path = os.path.join(self.path, folder_name)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        try:
            with open(file_link, "wb") as f:
                f.write(file.read())
        except Exception as e:
            logger.exception(e)
            return False

        return True

    @staticmethod
    def _generator_definition(iterable):
        """
        Python doesn't let to return and yield in one function,
        and always return generator
        """
        yield from iterable

    @contextlib.contextmanager
    def get_file(self, file_name: str) -> BinaryIO:
        """
        Get file for specific document from local-storage

        :param file_name: doc name

        :return: file-object
        """
        file_link = os.path.join(self.path, file_name)
        try:
            file_like = open(file_link, mode="rb")
        except Exception as e:
            logger.exception(e)
        else:
            yield file_like
            file_like.close()

    def download(
        self, file_name: str, return_iterator: bool = True
    ) -> Union[Iterator[bytes], bytes, None]:
        """
        Get file for specific document from local-storage

        :param file_name: link to document
        :param return_iterator: flag to return iterator
        of bytes or the whole file

        :return: file-iterator
        """
        file_link = os.path.join(self.path, file_name)

        try:
            with open(file_link, mode="rb") as file_like:
                if return_iterator:
                    return self._generator_definition(file_like.readlines())
                else:
                    return file_like.read()

        except FileNotFoundError as e:
            logger.exception(e)
            return None

    def delete(self, file_name: str):
        file_link = os.path.join(self.path, file_name)
        try:
            os.remove(file_link)
        except FileNotFoundError as e:
            logger.exception(e)

    def is_file_exists(self, file_name: str) -> bool:

        file_link = os.path.join(self.path, file_name)

        return os.path.exists(file_link)
