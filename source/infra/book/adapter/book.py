from typing import Optional

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

        response = requests.get(
            url=f"{self.__hostname}/subjects/{subject_param}.json",
            params={"offest": spec.page, "limit": spec.limit},
        )
        if response.status_code != 200:
            return GetBooksBySubjectAdapterResult(total=0, results=[])

        works = response.json()
        results = [
            Book(
                work_key=work["key"].rsplit("/", 1)[-1],
                title=work["title"],
                authors=[author_data["name"] for author_data in work["authors"]],
                edition_key=work["lending_edition"],
            )
            for work in works["works"]
        ]
        return GetBooksBySubjectAdapterResult(
            total=works["work_count"], results=results
        )

    def get_book_by_edition_key(self, edition_key: str) -> Optional[Book]:
        bibkeys = f"OLID:{edition_key}"
        response = requests.get(
            url=f"{self.__hostname}/api/books",
            params={
                "bibkeys": bibkeys,
                "jscmd": "details",
                "format": "json",
            },
        )
        if response.status_code != 200:
            return None

        response_json = response.json()
        if not response_json:
            return None

        details = response_json[bibkeys]["details"]
        return Book(
            work_key=details["works"][0]["key"].rsplit("/", 1)[-1],
            title=details["title"],
            authors=[author_data["name"] for author_data in details["authors"]],
            edition_key=edition_key,
        )
