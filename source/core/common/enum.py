from enum import Enum


class UserType(str, Enum):
    LIBRARIAN = "LIBRARIAN"
    MEMBER = "MEMBER"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
