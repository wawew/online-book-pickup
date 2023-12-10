from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from source.core.common.model import BookReservation


@dataclass
class ReserveBookSpec:
    edition_key: str
    pickup_time: datetime
    user_email: str
    reservation_start_time: datetime
    reservation_end_time: datetime


class IBookReservationService(ABC):
    @abstractmethod
    def reserve_book(self, spec: ReserveBookSpec) -> BookReservation:
        raise NotImplementedError
