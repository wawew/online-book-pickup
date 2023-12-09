from enum import Enum


class UserType(str, Enum):
    LIBRARIAN = "LIBRARIAN"
    MEMBER = "MEMBER"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class BookSubject(str, Enum):
    PHYSICS = "PHYSICS"
    MATHEMATICS = "MATHEMATICS"
    PROGRAMMING = "PROGRAMMING"
