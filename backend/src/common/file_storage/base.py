# stdlib
import pathlib
import tempfile
import typing
import zipfile
from abc import ABC, abstractmethod
from typing import BinaryIO, Iterator, Union


class BaseFileStorage(ABC):
    """Base class for working with file storage"""

    def get_file(self, file_name: str) -> BinaryIO:
        """get binary file content"""
        pass

    @abstractmethod
    def upload(self, *args, **kwargs):
        """save file to storage"""
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        """get file from storage"""
        pass

    def bulk_upload(self, files: dict[str, BinaryIO]) -> dict[str, bool]:
        """save many files to storage"""

        result = {}
        for file_name, file in files.items():
            result[file_name] = self.upload(file, file_name)

        return result

    def bulk_download(
        self, file_names: list[str], return_iterator: bool = True
    ) -> dict[str, Union[Iterator[bytes], bytes, None]]:
        """get many files from storage"""

        result = {}
        for file_name in file_names:
            result[file_name] = self.download(file_name, return_iterator)

        return result

    @abstractmethod
    def is_file_exists(self, file_name: str) -> bool:
        """Check if file exists."""
        pass

    @abstractmethod
    def delete(self, file_name: str):
        """delete file from storage"""
        pass

    def bulk_delete(self, file_names: set[str]):
        """delete many files from storage"""
        for file_name in file_names:
            self.delete(file_name)


class FileCompression:
    """Class for file compression"""

    @staticmethod
    def file_tree(
        path: pathlib.Path,
    ) -> typing.Generator[typing.Tuple[str, bytes], None, None]:
        """
        Get file tree from path

        :param path: path to directory

        :return: generator of file tree
        """

        for file in path.glob("**/*"):
            if file.is_file():
                yield file.relative_to(path), file.read_bytes()

    @staticmethod
    def zip_files(
        files_gen: typing.Generator[tuple[str, bytes], None, None],
    ) -> tempfile.SpooledTemporaryFile:
        """
        File compression without saving to disk

        :param files_gen: generator of files

        :return: zip file
        """
        tmpfile = tempfile.SpooledTemporaryFile()
        with zipfile.ZipFile(
            tmpfile, "w", compression=zipfile.ZIP_DEFLATED
        ) as zip_file:
            for file_path, file_content in files_gen:
                zip_file.writestr(str(file_path), file_content)

        tmpfile.seek(0)
        return tmpfile
