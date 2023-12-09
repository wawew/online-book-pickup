from injector import inject

from source.core.book.port.book_adapter import IBookAdapter
from source.core.book.port.book_service import (
    GetBooksBySubjectResult,
    GetBooksBySubjectSpec,
    IBookService,
)


class BookService(IBookService):
    @inject
    def __init__(self, book_adapter: IBookAdapter) -> None:
        self.book_adapter = book_adapter

    def get_books_by_subject(
        self, spec: GetBooksBySubjectSpec
    ) -> GetBooksBySubjectResult:
        books = self.book_adapter.get_books_by_subject(spec=spec)
        return GetBooksBySubjectResult(
            page=spec.page, limit=spec.limit, total=books.total, results=books.results
        )
