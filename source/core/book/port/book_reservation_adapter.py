from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from source.core.book.port.book_reservation_service import GetAllBookReservationsSpec
from source.core.common.model import Book, BookReservation


@dataclass
class GetReservedBooksByTimeSpec:
    edition_key: str
    reservation_start_time: datetime
    reservation_end_time: datetime


@dataclass
class CreateBookReservationSpec:
    book: Book
    pickup_time: datetime
    user_email: str
    reservation_start_time: datetime
    reservation_end_time: datetime


@dataclass
class GetBookReservationsAdapterResult:
    total: int
    results: List[BookReservation]


class IBookReservationAdapter(ABC):
    @abstractmethod
    def get_reserved_books_by_time(
        self, spec: GetReservedBooksByTimeSpec
    ) -> List[BookReservation]:
        raise NotImplementedError

    @abstractmethod
    def create_book_reservation(
        self, spec: CreateBookReservationSpec
    ) -> BookReservation:
        raise NotImplementedError

    @abstractmethod
    def get_book_reservations(
        self, spec: GetAllBookReservationsSpec
    ) -> GetBookReservationsAdapterResult:
        raise NotImplementedError
