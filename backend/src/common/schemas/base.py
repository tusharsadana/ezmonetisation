# stdlib
import abc

# thirdparty
import orjson
from pydantic import BaseModel as PydanticModel


def orjson_dumps(v, *, default):
    """json dumps method to update base lib method"""
    return orjson.dumps(v, default=default).decode()


class BaseModel(PydanticModel):
    """
    Base pydantic model with updated json-methods

    orjson gets faster working with json than base lib
    """

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True


class ListContentIterationMixin(abc.ABC):
    __root__: list = None

    def __iter__(self):
        return iter(self.__root__)
