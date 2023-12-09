from typing import no_type_check

from injector import Binder, Module, singleton

from source.core.book.port.book_adapter import IBookAdapter
from source.infra.book.adapter.book import OpenLibraryBookAdapter


class BookAdapterModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=IBookAdapter, to=OpenLibraryBookAdapter, scope=singleton)
