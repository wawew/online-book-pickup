from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from source.core.book.port.book_service import GetBooksBySubjectSpec
from source.core.common.model import Book


@dataclass
class GetBooksBySubjectAdapterResult:
    total: int
    results: List[Book]


class IBookAdapter(ABC):
    @abstractmethod
    def get_books_by_subject(
        self, spec: GetBooksBySubjectSpec
    ) -> GetBooksBySubjectAdapterResult:
        raise NotImplementedError

    @abstractmethod
    def get_book_by_edition_key(self, edition_key: str) -> Optional[Book]:
        raise NotImplementedError
