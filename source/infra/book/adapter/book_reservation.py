from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from source.core.book.port.book_reservation_adapter import (
    CreateBookReservationSpec,
    GetBookReservationsAdapterResult,
    GetReservedBooksByTimeSpec,
    IBookReservationAdapter,
)
from source.core.book.port.book_reservation_service import GetAllBookReservationsSpec
from source.core.common.model import BookReservation


class LocalStorageBookReservationAdapter(IBookReservationAdapter):
    def __init__(self) -> None:
        self.__local_data = self.__initiate_local_data()

    def get_reserved_books_by_time(
        self, spec: GetReservedBooksByTimeSpec
    ) -> List[BookReservation]:
        return list(
            filter(lambda x: self.__is_book_reserved(x, spec), self.__local_data)
        )

    def create_book_reservation(
        self, spec: CreateBookReservationSpec
    ) -> BookReservation:
        book_reservation = BookReservation(
            key=uuid4().hex,
            book=spec.book,
            pickup_time=spec.pickup_time,
            user_email=spec.user_email,
            reservation_start_time=spec.reservation_start_time,
            reservation_end_time=spec.reservation_end_time,
            created_at=datetime.now(tz=timezone.utc),
            created_by=spec.user_email,
        )
        self.__local_data.append(book_reservation)
        return book_reservation

    def get_book_reservations(
        self, spec: GetAllBookReservationsSpec
    ) -> GetBookReservationsAdapterResult:
        offset_value = (spec.page - 1) * spec.limit
        return GetBookReservationsAdapterResult(
            total=len(self.__local_data),
            results=self.__local_data[offset_value : offset_value + spec.limit],
        )

    def __initiate_local_data(self) -> List[BookReservation]:
        return []

    @staticmethod
    def __is_book_reserved(
        book_reservation: BookReservation, spec: GetReservedBooksByTimeSpec
    ) -> bool:
        if book_reservation.book.edition_key != spec.edition_key:
            return False
        if max(
            book_reservation.reservation_start_time, spec.reservation_start_time
        ) >= min(book_reservation.reservation_end_time, spec.reservation_end_time):
            return False
        return True
