# stdlib
import dataclasses


@dataclasses.dataclass
class RedisSearchIndex:
    @classmethod
    def default_schema(cls):
        return [field.default for field in dataclasses.fields(cls)]
