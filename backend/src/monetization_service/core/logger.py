# stdlib
import json
import logging

# thirdparty
from uvicorn.logging import DefaultFormatter

# project
from src.monetization_service.core.constants import COMMON_RECORD_ATTRS


class ConsoleDefaultFormatter(DefaultFormatter):
    """
    Console formatter
    """

    @staticmethod
    def _make_extra(record):
        """Pack extra dict"""

        extra = {}
        for key, val in record.__dict__.items():
            if key not in COMMON_RECORD_ATTRS:
                extra[key] = val
        return extra

    def format(self, record: logging.LogRecord) -> str:
        """Format log to proper format"""

        extra_info = self._make_extra(record)
        record.extra = ""
        if extra_info:
            record.extra = json.dumps(
                extra_info, ensure_ascii=False, default=str
            )
        text = super().format(record)
        if not record.extra and not record.exc_text:
            text = text[:-2]

        return text
