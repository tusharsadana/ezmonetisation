# stdlib
from typing import Optional, Union
from uuid import UUID

# thirdparty
from pydantic import Field, root_validator

# project
from src.common.schemas.base import BaseModel, ListContentIterationMixin
from src.common.schemas.extraction_task import ModelsInfo
from src.common.schemas.preprocessing_result import PageTokens


class Impact(BaseModel):
    """Schema for impact of entity on document"""

    value: str = Field(title="Impact of entity")
    available_impacts: list[str]


class Entity(BaseModel):
    """Schema for extracted entities from documents"""

    raw_text: str = Field(
        title="Text extracted from document as an entity", alias="rawText"
    )
    normalized_text: str = Field(
        title="Formatted or cleared entity "
        "text e.g. formatted date - DD.MM.YY",
        alias="normalizedText",
    )
    score: float
    question: str
    tokens: PageTokens = Field(title="Only tokens connected with the entities")
    selected: bool = Field(default=False, title="Entity was selected by user")
    impact: Union[Impact, None] = Field(title="Impact of entity")
    entry_id: int


class Entities(ListContentIterationMixin, BaseModel):
    """Schema for all entities with  tokens"""

    __root__: list[Entity]

    @root_validator
    def make_one_selected_by_entry(cls, values):
        """Make first selected by entry_id"""

        all_entities = values.get("__root__")
        selected_by_entry_id = {}

        for i, entity in enumerate(all_entities):

            if entity.entry_id in selected_by_entry_id:
                continue

            values["__root__"][i].selected = True
            selected_by_entry_id[entity.entry_id] = True

        return values


class EntitiesTypes(BaseModel):
    """Schema for all entities types with entities and tokens"""

    __root__: dict[str, Entities]

    class Config:
        schema_extra = {
            "example": {
                "Due Date": [
                    {
                        "rawText": " July 16, 2021",
                        "normalizedText": "7-16-2021",
                        "score": 0.9994159936904907,
                        "question": "When money transfer should be done?",
                        "tokens": [
                            {
                                "pageId": 0,
                                "text": "July",
                                "tokenId": 222,
                                "bBox": {
                                    "xMin": 302.7606,
                                    "yMin": 540.4872,
                                    "xMax": 321.083172,
                                    "yMax": 550.5072,
                                },
                            },
                            {
                                "pageId": 0,
                                "text": "16,",
                                "tokenId": 223,
                                "bBox": {
                                    "xMin": 323.573142,
                                    "yMin": 540.4872,
                                    "xMax": 336.098142,
                                    "yMax": 550.5072,
                                },
                            },
                            {
                                "pageId": 0,
                                "text": "2021",
                                "tokenId": 224,
                                "bBox": {
                                    "xMin": 338.54001600000004,
                                    "yMin": 540.4872,
                                    "xMax": 358.574004,
                                    "yMax": 550.5072,
                                },
                            },
                        ],
                        "selected": True,
                    }
                ],
                "Document Date": [
                    {
                        "rawText": " July 1, 2021",
                        "normalizedText": "7-1-2021",
                        "score": 0.999337375164032,
                        "question": "Which is document date?",
                        "tokens": [
                            {
                                "pageId": 0,
                                "text": "July",
                                "tokenId": 0,
                                "bBox": {
                                    "xMin": 73.2024,
                                    "yMin": 112.44731999999999,
                                    "xMax": 89.897724,
                                    "yMax": 122.46731999999997,
                                },
                            },
                            {
                                "pageId": 0,
                                "text": "1,",
                                "tokenId": 1,
                                "bBox": {
                                    "xMin": 92.399718,
                                    "yMin": 112.44731999999999,
                                    "xMax": 99.896682,
                                    "yMax": 122.46731999999997,
                                },
                            },
                            {
                                "pageId": 0,
                                "text": "2021",
                                "tokenId": 2,
                                "bBox": {
                                    "xMin": 102.34056,
                                    "yMin": 112.44731999999999,
                                    "xMax": 122.374548,
                                    "yMax": 122.46731999999997,
                                },
                            },
                        ],
                        "selected": True,
                    }
                ],
                "Remaining Commitment": [
                    {
                        "rawText": " $1,905,765.01",
                        "normalizedText": "1,905,765.01",
                        "score": 0.9989741444587708,
                        "question": "What is amount of the total unfunded "
                        "commitment?",
                        # noqa
                        "tokens": [
                            {
                                "pageId": 1,
                                "text": "$1,905,765.01",
                                "tokenId": 47,
                                "bBox": {
                                    "xMin": 302.52936,
                                    "yMin": 217.4529,
                                    "xMax": 359.992056,
                                    "yMax": 227.47289999999998,
                                },
                            }
                        ],
                        "selected": True,
                    }
                ],
                "Fund Name": [
                    {
                        "rawText": " Accel-KKR Credit Partners,",
                        "normalizedText": "Accel-KKR Credit Partners,",
                        "score": 0.4103277921676636,
                        "question": "What is a name of fund?",
                        "tokens": [
                            {
                                "pageId": 1,
                                "text": "Accel-KKR",
                                "tokenId": 87,
                                "bBox": {
                                    "xMin": 72,
                                    "yMin": 389.17938000000004,
                                    "xMax": 119.86353600000001,
                                    "yMax": 399.19938,
                                },
                            },
                            {
                                "pageId": 1,
                                "text": "Credit",
                                "tokenId": 88,
                                "bBox": {
                                    "xMin": 122.384568,
                                    "yMin": 389.17938000000004,
                                    "xMax": 147.317334,
                                    "yMax": 399.19938,
                                },
                            },
                            {
                                "pageId": 1,
                                "text": "Partners,",
                                "tokenId": 89,
                                "bBox": {
                                    "xMin": 149.838366,
                                    "yMin": 389.17938000000004,
                                    "xMax": 185.041632,
                                    "yMax": 399.19938,
                                },
                            },
                        ],
                        "selected": True,
                    }
                ],
                "Client / Plan Name": [
                    {
                        "rawText": " ($543,103.45)",
                        "normalizedText": "($543,103.45)",
                        "score": 0.4751620590686798,
                        "question": "What is a Client/ Plan name?",
                        "tokens": [
                            {
                                "pageId": 1,
                                "text": "($543,103.45)",
                                "tokenId": 34,
                                "bBox": {
                                    "xMin": 303.33897599999995,
                                    "yMin": 191.05020000000002,
                                    "xMax": 360.00107399999996,
                                    "yMax": 201.0702,
                                },
                            }
                        ],
                        "selected": True,
                    }
                ],
            }
        }


class PredictedDocumentType(BaseModel):
    type: str = Field(alias="documentType")
    score: float
    available_types: list[str]


class Currency(BaseModel):
    value: Union[str, None] = Field(default="USD")
    available_currencies: list[str]


class ModelResult(BaseModel):
    """Result from inference backend model"""

    entities: EntitiesTypes
    doc_type: PredictedDocumentType = Field(alias="documentType")
    currency: Currency


class ExtractionResult(BaseModel):
    """Result from inference backend"""

    task_id: UUID = Field(alias="taskId")
    doc_id: UUID = Field(alias="docId")
    model_result: Optional[ModelResult] = Field(alias="modelResult")
    error: Optional[str]
    models_info: ModelsInfo = Field(alias="modelsInfo")
