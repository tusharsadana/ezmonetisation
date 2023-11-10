# stdlib
from enum import Enum
from typing import Mapping, Optional

# project
from src.common.schemas.base import BaseModel

# Attributes for filter logs
COMMON_RECORD_ATTRS = frozenset(
    (
        "args",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "lineno",
        "message",
        "module",
        "msecs",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "report",
        "color_message",
        "relativeCreated",
        "stack",
        "tags",
        "thread",
        "threadName",
        "stack_info",
        "asctime",
        "extra",
        "extra_info",
        "client_addr",
        "request_line",
        "status_code",
    )
)


class ModelType(str, Enum):
    classification = "classification"
    denoising = "denoising"
    qa = "qa"

    @staticmethod
    def get(value: str) -> Optional["ModelType"]:
        res = [i for i in ModelType if i.value == value]
        return res[0] if len(res) == 1 else None

    @staticmethod
    def list():
        return [i.value for i in ModelType]


class ModelsInfo(BaseModel):
    __root__: Mapping[ModelType, str]


class StorageType(str, Enum):
    s3 = "s3"
    local = "local"


class ServiceName(str, Enum):
    monetization = "monetization"


class DeploymentType(str, Enum):
    k8s = "k8s"
    instance = "instance"
