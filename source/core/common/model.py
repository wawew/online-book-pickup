from dataclasses import dataclass
from datetime import datetime
from typing import List

from source.core.common.enum import UserStatus, UserType


@dataclass
class BaseModel:
    created_at: datetime
    created_by: str


@dataclass
class User(BaseModel):
    email: str
    user_type: UserType
    status: UserStatus
    salt: str
    credential: str


@dataclass
class Book:
    work_key: str
    title: str
    authors: List[str]
    edition_key: str


@dataclass
class BookReservation(BaseModel):
    key: str
    book: Book
    pickup_time: datetime
    user_email: str
    reservation_start_time: datetime
    reservation_end_time: datetime


@dataclass
class PaginationSpec:
    page: int
    limit: int


@dataclass
class PaginationResult(PaginationSpec):
    total: int
