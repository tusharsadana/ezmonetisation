# stdlib
from uuid import UUID

# project
from src.common.schemas.base import BaseModel


class PreprocessingTask(BaseModel):
    doc_id: UUID
    task_id: UUID
    file_name: str
    file_path: str
