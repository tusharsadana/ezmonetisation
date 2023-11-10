# stdlib
import json
import os.path
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional


@dataclass
class QuestionsList:
    use_n_questions: int
    questions: List[str]


@dataclass
class EntityImpact:
    default_impact: str
    available_impacts: List[str]


@dataclass
class EntityReconciliation:
    default_value: str
    available_values: List[str]


class EntityConfigurator:
    """
    Verify project config file, collect all the questions and
    dependencies between entity types, document types and questions.
    config_file_path: str - path to file with project config

    Available_attributes
    --------------------
    config_raw_data: dict - raw data from config file
    config_name: str - name of the config

    available_document_types: List[str] - list of available document types
    _available_entity_types: List[str] - list of available entity types
    entities: List[str] - list of available entity types

    entity_questions_map: dict - map entity type to list of questions
    entities2questions: dict - map entity type to list of questions (interface)

    entity_major_type_map: dict - map entity type to major type
    document_type_entity_type_map: dict - map document type to list of
    entity types
    available_currencies: List[str] - list of available currencies
    entity_impact: dict - map entity type to EntityImpact object
    entities2reconciliation: dict - map entity type to EntityReconciliation
    object
    """

    def __init__(self, config_file_path: str):
        if not os.path.exists(config_file_path):
            raise FileExistsError(
                f"Config file does not exist: {config_file_path}"
            )

        self.config_raw_data = None
        try:
            with open(config_file_path) as fr:
                self.config_raw_data = json.load(fr)
        except Exception as e:
            raise IOError(
                f"Unable to open file {config_file_path}, error message: {e}"
            )

        self._verify_config_keys()
        self._verify_available_document_type()
        self._verify_entities_and_questions()
        self._load_entity_impact()
        self._load_reconciliation()
        self._verify_available_entity_types()

    def _verify_config_keys(self):
        needed_keys = {
            "config_name",
            "available_document_types",
            "available_entity_type",
            "document_type_entity_type_map",
            "entity_type_questions_map",
            "available_currencies",
        }

        for needed_key in needed_keys:
            if needed_key not in self.config_raw_data:
                raise KeyError(
                    f"Needed key {needed_key} not found in config file"
                )

    def _verify_available_document_type(self):

        available_document_types = self.config_raw_data[
            "available_document_types"
        ]

        if len(available_document_types) != len(set(available_document_types)):
            raise ValueError(
                f"All values of available_document_types should be unique,"
                f" but {Counter(available_document_types)}"
            )

        self.available_document_types = list(set(available_document_types))

        document_type_entity_type_map = self.config_raw_data[
            "document_type_entity_type_map"
        ]
        for doc_type in available_document_types:
            if doc_type not in document_type_entity_type_map:
                raise KeyError(
                    f"Can not find list of entities for document type "
                    f"{doc_type}"
                )

        self.document_type_entity_type_map = document_type_entity_type_map

    def _verify_available_entity_types(self):
        available_entity_types_raw = self.config_raw_data[
            "available_entity_type"
        ]
        available_entity_types = [
            i["entity_name"] for i in available_entity_types_raw
        ]
        if len(available_entity_types) != len(set(available_entity_types)):
            raise ValueError(
                f"All values of available_entity_types should be unique,"
                f" but {Counter(available_entity_types)}"
            )

        self.available_entity_types = list(set(available_entity_types))

    def _verify_entities_and_questions(self):
        entity_types = self.config_raw_data["available_entity_type"]
        entity_type_questions_map = self.config_raw_data[
            "entity_type_questions_map"
        ]
        self.entity_questions_map = {}
        self.entity_major_type_map = {}
        self.multiple_entry_entities = []  # entity can have multiple entries for document
        self.single_entry_entities = []  # entity can have single entry for document

        for ent_info in entity_types:
            ent_name = ent_info.get("entity_name")
            if ent_name is None:
                raise ValueError(
                    f"Entity name can not be None, but {ent_info}"
                )

            if ent_name not in entity_type_questions_map:
                raise KeyError(
                    f"Can not find question for entity type {ent_name}"
                )

            n_questions = ent_info.get("use_n_questions")
            if n_questions is None:
                raise ValueError(
                    f"N_questions can not be None, but {ent_info}"
                )

            entity_major_type = ent_info.get("type")
            self.entity_major_type_map[ent_name] = entity_major_type

            is_multiple = ent_info.get("is_multiple")
            if is_multiple is None:
                raise ValueError(
                    f"is_multiple can not be None, but {ent_info}"
                )
            if is_multiple:
                self.multiple_entry_entities.append(ent_name)
            else:
                self.single_entry_entities.append(ent_name)

            actual_questions_number = len(entity_type_questions_map[ent_name])
            if actual_questions_number < n_questions:
                raise ValueError(
                    f"n_questions: {n_questions} can not be greater than "
                    f"the number of predefined questions: "
                    f"{actual_questions_number}"
                )

            self.entity_questions_map[ent_name] = QuestionsList(
                n_questions, entity_type_questions_map[ent_name]
            )

    def get_ent_types_for_doc_type(self, document_type: str) -> List[str]:
        if document_type not in self.document_type_entity_type_map:
            raise TypeError(
                f"Can not find document type {document_type}, "
                f"available types {self.document_type_entity_type_map}"
            )
        return self.document_type_entity_type_map[document_type]

    def get_questions_by_ent_type(
        self, entity_type: str, n_questions: Optional[int] = None
    ) -> List[str]:
        if entity_type not in self.entity_questions_map:
            raise TypeError(
                f"Can not find entity type {entity_type}, "
                f"available types {list(self.entity_questions_map.keys())}"
            )
        if n_questions is None:
            qs_list = self.entity_questions_map[entity_type]
            questions = qs_list.questions[: qs_list.use_n_questions]
            return questions
        if n_questions == -1:
            qs_list = self.entity_questions_map[entity_type]
            return qs_list.questions

        actual_questions_number = len(
            self.entity_questions_map[entity_type].questions
        )
        if actual_questions_number < n_questions:
            raise ValueError(
                f"n_questions: {n_questions} can not be greater than "
                f"the number of predefined questions: "
                f"{actual_questions_number}"
            )
        return self.entity_questions_map[entity_type].questions[:n_questions]

    @property
    def entities(self):
        return list(self.entity_questions_map.keys())

    @property
    def entities2questions(self):
        entities2questions = {}
        for entity_type in self.entity_questions_map:
            qs_list = self.entity_questions_map[entity_type]
            questions = qs_list.questions[: qs_list.use_n_questions]
            entities2questions[entity_type] = questions
        return entities2questions

    @property
    def available_currencies(self):
        # TODO: suggestion: have you considered to put everything from config
        #  to some dataclass when class initialize instead of using dict keys.
        #  It could be easier to change config names
        #  I guess(IDE will help to change all config occurrences in code)
        return self.config_raw_data["available_currencies"]

    @property
    def get_amount_entities(self):
        return [
            ent
            for ent in self.entities
            if self.entity_major_type_map[ent] == "amount"
        ]

    def _load_entity_impact(self):
        raw_entity_impact_mapping = self.config_raw_data["entity_impact"]
        self.entity_impact = {}
        if raw_entity_impact_mapping:
            inter = set(raw_entity_impact_mapping.keys()) & set(
                self.entity_questions_map.keys()
            )
            if len(inter) != len(raw_entity_impact_mapping.keys()):
                raise ValueError(
                    "Not all entities from entity_impact are "
                    "presented in available_entity_type"
                )
            for ent_type, raw_values in raw_entity_impact_mapping.items():
                self.entity_impact[ent_type] = EntityImpact(
                    default_impact=raw_values["default_impact"],
                    available_impacts=raw_values["available_impacts"],
                )

    def _load_reconciliation(self):
        raw_reconciliation_mapping = self.config_raw_data.get("reconciliation")
        self.entities2reconciliation = {}
        if raw_reconciliation_mapping:
            inter = [
                ent_type
                for ent_type in raw_reconciliation_mapping.keys()
                if ent_type not in self.entity_questions_map.keys()
            ]

            if inter:
                raise ValueError(
                    "Not all entities from reconciliation are "
                    "presented in available_entity_type"
                )
            for ent_type, raw_values in raw_reconciliation_mapping.items():
                self.entities2reconciliation[ent_type] = EntityReconciliation(
                    default_value=raw_values["default_value"],
                    available_values=raw_values["available_values"],
                )


@lru_cache
def get_entity_configurator(config_file_path: str) -> EntityConfigurator:
    return EntityConfigurator(config_file_path)
