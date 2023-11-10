# stdlib
from enum import Enum, IntEnum

# project


class StrEnum(str, Enum):
    pass


class Permission(StrEnum):
    pass


class RoleName(StrEnum):
    """Role names"""

    MEMBER = "member"
    ADMIN = "admin"


PERMISSIONS_PER_ROLE = {
    "member": [],
    "admin": [],
}



