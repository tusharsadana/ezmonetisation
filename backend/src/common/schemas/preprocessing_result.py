# stdlib
from typing import Optional, Union
from uuid import UUID

# thirdparty
from pydantic import Field

# project
from src.common.schemas.base import BaseModel, ListContentIterationMixin


class Bbox(BaseModel):
    """Rectangle coordinates for text"""

    x_min: float = Field(title="Top left x", alias="xMin")
    y_min: float = Field(title="Top left y", alias="yMin")
    x_max: float = Field(title="Down right x", alias="xMax")
    y_max: float = Field(title="Down right y", alias="yMax")


class PageToken(BaseModel):
    """Schema for one page"""

    page_id: int = Field(alias="pageId")
    token_uuid: Union[UUID, None] = Field(alias="tokenUuid")
    text: str
    token_id: int = Field(alias="tokenId")
    bbox: Bbox = Field(title="Rectangle area of text", alias="bBox")


class PageTokens(ListContentIterationMixin, BaseModel):
    __root__: list[PageToken]


class Page(BaseModel):
    """Schema for one page"""

    width: int
    height: int
    tokens: Optional[PageTokens] = None

    def __init__(self, **data):
        if "tokens" in data and data["tokens"] is None:
            data["tokens"] = PageTokens(__root__=[])
        super().__init__(**data)


class Pages(ListContentIterationMixin, BaseModel):
    """Schema for all pages with tokens"""

    __root__: list[Page]


class Links(BaseModel):
    file: str = Field(title="Absolute Link to converted file")
    images: list[str] = Field(
        title="List with Absolute Link to images for document"
    )


class ModelResult(BaseModel):
    """Result from inference backend model"""

    pages: Pages
    links: Links


class PreprocessingResult(BaseModel):
    """Result from preprocessing service"""

    task_id: UUID = Field(alias="taskId")
    doc_id: UUID = Field(alias="docId")
    model_result: Optional[ModelResult] = Field(alias="modelResult")
    error: Optional[str]

    class Config:
        allow_population_by_field_name = True
