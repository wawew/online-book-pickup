from datetime import datetime, timezone

from injector import inject

from source.core.book.port.book_adapter import IBookAdapter
from source.core.book.port.book_reservation_adapter import (
    CreateBookReservationSpec,
    GetReservedBooksByTimeSpec,
    IBookReservationAdapter,
)
from source.core.book.port.book_reservation_service import (
    GetAllBookReservationsResult,
    GetAllBookReservationsSpec,
    IBookReservationService,
    ReserveBookSpec,
)
from source.core.common.exception import EntityNotFoundException, GenericException
from source.core.common.model import BookReservation


class BookReservationService(IBookReservationService):
    @inject
    def __init__(
        self,
        book_reservation_adapter: IBookReservationAdapter,
        book_adapter: IBookAdapter,
    ) -> None:
        self.book_reservation_adapter = book_reservation_adapter
        self.book_adapter = book_adapter

    def reserve_book(self, spec: ReserveBookSpec) -> BookReservation:
        self.__validate_reserve_book(spec=spec)
        book = self.book_adapter.get_book_by_edition_key(edition_key=spec.edition_key)
        if not book:
            raise EntityNotFoundException(
                entity="Book", entity_id_name="edition_key", entity_id=spec.edition_key
            )
        return self.book_reservation_adapter.create_book_reservation(
            spec=CreateBookReservationSpec(
                book=book,
                pickup_time=spec.pickup_time,
                user_email=spec.user_email,
                reservation_start_time=spec.reservation_start_time,
                reservation_end_time=spec.reservation_end_time,
            )
        )

    def get_all_book_reservations(
        self, spec: GetAllBookReservationsSpec
    ) -> GetAllBookReservationsResult:
        book_reservations = self.book_reservation_adapter.get_book_reservations(
            spec=spec
        )
        return GetAllBookReservationsResult(
            page=spec.page,
            limit=spec.limit,
            total=book_reservations.total,
            results=book_reservations.results,
        )

    def __validate_reserve_book(self, spec: ReserveBookSpec) -> None:
        if spec.reservation_start_time < datetime.now(tz=timezone.utc):
            raise GenericException("Reservation time cannot be set to past time")
        if spec.reservation_start_time >= spec.reservation_end_time:
            raise GenericException(
                "Reservation end time must be greater than start time"
            )
        if (
            spec.pickup_time < spec.reservation_start_time
            or spec.pickup_time >= spec.reservation_end_time
        ):
            raise GenericException("Pickup time must be within reservation time")

        book_reservations = self.book_reservation_adapter.get_reserved_books_by_time(
            spec=GetReservedBooksByTimeSpec(
                edition_key=spec.edition_key,
                reservation_start_time=spec.reservation_start_time,
                reservation_end_time=spec.reservation_end_time,
            )
        )
        if book_reservations:
            raise GenericException(
                f"Book reservation for edition_key {spec.edition_key} is not available. "
                "Please try other reservation time."
            )
