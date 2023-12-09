import requests

from source.core.book.port.book_adapter import (
    GetBooksBySubjectAdapterResult,
    IBookAdapter,
)
from source.core.book.port.book_service import GetBooksBySubjectSpec
from source.core.common.enum import BookSubject
from source.core.common.model import Book


class OpenLibraryBookAdapter(IBookAdapter):
    __hostname = "https://openlibrary.org"
    __book_subject_to_param = {
        BookSubject.MATHEMATICS: "mathematics",
        BookSubject.PHYSICS: "physics",
        BookSubject.PROGRAMMING: "programming",
    }

    def get_books_by_subject(
        self, spec: GetBooksBySubjectSpec
    ) -> GetBooksBySubjectAdapterResult:
        subject_param = self.__book_subject_to_param.get(spec.subject)
        if not subject_param:
            return GetBooksBySubjectAdapterResult(total=0, results=[])

        response_json = requests.get(
            url=f"{self.__hostname}/subjects/{subject_param}.json",
            params={"offest": spec.page, "limit": spec.limit},
        ).json()
        results = [
            Book(
                key=work["key"].rsplit("/", 1)[-1],
                title=work["title"],
                authors=[author_data["name"] for author_data in work["authors"]],
                edition=work["lending_edition"],
            )
            for work in response_json["works"]
        ]
        return GetBooksBySubjectAdapterResult(
            total=response_json["work_count"], results=results
        )
