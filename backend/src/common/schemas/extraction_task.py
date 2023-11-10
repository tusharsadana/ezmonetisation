# stdlib
from enum import Enum
from typing import Mapping, Optional
from uuid import UUID

# thirdparty
from pydantic import Field

# project
from src.common.schemas.base import BaseModel
from src.common.schemas.preprocessing_result import ModelResult


class ModelType(str, Enum):
    qa = "qa"
    classification = "classification"
    denoising = "denoising"


class ModelsInfo(BaseModel):
    __root__: Mapping[str, str]


class ExtractionTask(BaseModel):
    doc_id: UUID = Field(alias="docId")
    task_id: UUID = Field(alias="taskId")
    model_result: Optional[ModelResult] = Field(alias="modelResult")
    models_info: ModelsInfo = Field(alias="modelsInfo")
