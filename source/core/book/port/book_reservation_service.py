from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from source.core.common.model import BookReservation, PaginationResult, PaginationSpec


@dataclass
class ReserveBookSpec:
    edition_key: str
    pickup_time: datetime
    user_email: str
    reservation_start_time: datetime
    reservation_end_time: datetime


@dataclass
class GetAllBookReservationsSpec(PaginationSpec):
    pass


@dataclass
class GetAllBookReservationsResult(PaginationResult):
    results: List[BookReservation]


class IBookReservationService(ABC):
    @abstractmethod
    def reserve_book(self, spec: ReserveBookSpec) -> BookReservation:
        raise NotImplementedError

    @abstractmethod
    def get_all_book_reservations(
        self, spec: GetAllBookReservationsSpec
    ) -> GetAllBookReservationsResult:
        raise NotImplementedError
