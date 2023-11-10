# stdlib
import os
import typing
from functools import cache
from secrets import token_hex

# thirdparty
from fastapi import status
from fastapi.responses import ORJSONResponse, Response

# project
from src.common.entity_configurator import get_entity_configurator
from src.monetization_service.settings.development import settings


def generate_random_string() -> str:
    return token_hex(6)


@cache
def get_ent_config_path() -> str:
    config_name = os.environ.get(
        "ENTITY_CONFIG_NAME", "mercer_contrib_distrib_config.json"
    )
    if config_name is None:
        raise KeyError(
            '"ENTITY_CONFIG_NAME" is not set, can not start consumer'
        )
    config_dir = os.path.join(settings.project_dir, "common/project_configs/")
    return os.path.join(config_dir, config_name)


entity_configurator = get_entity_configurator(get_ent_config_path())


def list_paginator(
    list_obj: typing.Sequence[typing.Any], page_number: int, num=10
) -> typing.Generator[typing.Any, None, None]:
    """
    Paginator for list objects

    :param list_obj: list object
    :param page_number: page number
    :param num: number of objects per page

    :return: generator of objects
    """
    size = len(list_obj)
    start = (page_number - 1) * num
    end = page_number * num
    for i in range(start, end):
        if i >= size or i < 0:
            break
        yield list_obj[i]


def error_check_api(result: dict):
    try:
        if "error" in result:
            status_code = result.get("status_code")
            if status_code == status.HTTP_204_NO_CONTENT:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                return ORJSONResponse(
                    status_code=status_code,
                    content={"detail": result["error"]},
                )
    except KeyError:
        return None
