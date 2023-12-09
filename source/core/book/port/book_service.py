from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from source.core.common.enum import BookSubject
from source.core.common.model import Book, PaginationResult, PaginationSpec


@dataclass
class GetBooksBySubjectSpec(PaginationSpec):
    subject: BookSubject


@dataclass
class GetBooksBySubjectResult(PaginationResult):
    results: List[Book]


class IBookService(ABC):
    @abstractmethod
    def get_books_by_subject(
        self, spec: GetBooksBySubjectSpec
    ) -> GetBooksBySubjectResult:
        raise NotImplementedError
