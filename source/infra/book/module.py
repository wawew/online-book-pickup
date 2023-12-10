from typing import no_type_check

from injector import Binder, Module, singleton

from source.core.book.port.book_adapter import IBookAdapter
from source.core.book.port.book_reservation_adapter import IBookReservationAdapter
from source.infra.book.adapter.book import OpenLibraryBookAdapter
from source.infra.book.adapter.book_reservation import (
    LocalStorageBookReservationAdapter,
)


class BookAdapterModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=IBookAdapter, to=OpenLibraryBookAdapter, scope=singleton)
        binder.bind(
            interface=IBookReservationAdapter,
            to=LocalStorageBookReservationAdapter,
            scope=singleton,
        )
