# stdlib
import logging
import os
import zipfile
from typing import Optional

# project
from src.common.file_storage.base import BaseFileStorage
from src.common.schemas.extraction_result import ModelsInfo
from src.common.schemas.extraction_task import ModelType

logger = logging.getLogger(__name__)


class Versioniser:
    def __init__(self, weights_path: str):
        self.weights_path = weights_path
        self.current_model_versions = {
            model_type.value: self._load_version(
                os.path.join(self.weights_path, "current", model_type)
            )
            for model_type in ModelType
        }
        self.upload_in_progress = set()

    @staticmethod
    def _load_version(model_path: str) -> Optional[str]:
        """Load version from file in model_folder"""
        try:
            with open(os.path.join(model_path, "VERSION.TXT")) as f:
                version = f.readline()

                if version:
                    version = version.rstrip("\n")

        except FileNotFoundError:
            logger.error("Version in path = %s is not found" % model_path)
            return None
        return version

    def _transfer_delete_folders(self, model_type):
        """Delete old files and transfer model from new to current folder in local storage"""

        source = os.path.join(self.weights_path, "new", model_type)
        destination = os.path.join(self.weights_path, "current", model_type)

        new_files = os.listdir(source)
        old_files = os.listdir(destination)

        # delete old files
        for f in old_files:
            os.remove(os.path.join(destination, f))

        # add new files
        for f in new_files:
            src_path = os.path.join(source, f)
            dst_path = os.path.join(destination, f)

            os.rename(src_path, dst_path)

        new_files = os.listdir(source)
        # delete old files
        for f in new_files:
            os.remove(os.path.join(source, f))

    @staticmethod
    def _download_func(
        weights_path: str,
        model_type: str,
        model_version,
        file_storage: BaseFileStorage,
    ):
        """Download func of model from S3"""

        file_name = model_type + "_" + model_version + ".zip"
        file_iterator = file_storage.download(file_name)

        if not os.path.exists(weights_path):
            os.makedirs(weights_path)

        if not os.path.exists(os.path.join(weights_path, "new")):
            os.makedirs(os.path.join(weights_path, "new"))

        if not os.path.exists(os.path.join(weights_path, "new", model_type)):
            os.makedirs(os.path.join(weights_path, "new", model_type))

        zip_file_path = os.path.join(
            weights_path, "new", model_type, "temp.zip"
        )

        with open(zip_file_path, "wb") as f:
            for chunk in file_iterator:
                f.write(chunk)

        with zipfile.ZipFile(zip_file_path, "r") as z:
            z.extractall(os.path.join(weights_path, "new", model_type))

        os.remove(zip_file_path)

    def _download_model_from_s3(
        self, model_type: str, model_version, file_storage: BaseFileStorage
    ):
        """Download files of model from S3"""

        self.upload_in_progress.add(model_type)

        logger.info(
            "Add model %s %s to in progress" % (model_type, model_version)
        )

        self._download_func(
            self.weights_path, model_type, model_version, file_storage
        )

        logger.info(
            "Delete model %s %s  from in progress"
            % (model_type, model_version)
        )

        self.upload_in_progress.remove(model_type)

    async def check_update_version(
        self, models_info: ModelsInfo, file_storage: BaseFileStorage
    ):
        """Check and update version of models"""

        models_to_upload = []

        for model_type, new_model_version in models_info.__root__.items():

            # old_model
            if new_model_version == self.current_model_versions[model_type]:
                continue
            logger.warning(
                "New version %s of %s model has come to verification and s3"
                % (new_model_version, model_type)
            )
            new_model_version_local = self._load_version(
                os.path.join(self.weights_path, "new", model_type)
            )
            # new_version exists, but is not loaded to local storage yet
            if (
                not new_model_version_local
                or new_model_version_local != new_model_version
            ):
                logger.warning(
                    "Version %s is not loaded to local storage yet"
                    % new_model_version
                )

                if model_type not in self.upload_in_progress:
                    logger.info("Start downloading of model %s" % model_type)
                    # create_task_to_load_model from s3
                    self._download_model_from_s3(
                        model_type, new_model_version, file_storage
                    )
                else:
                    logger.info(
                        "Download of model %s is in progress" % model_type
                    )
                    continue

            self._transfer_delete_folders(model_type)

            self.current_model_versions[model_type] = new_model_version
            models_to_upload.append(model_type)

        return models_to_upload
