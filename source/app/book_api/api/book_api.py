from typing import List

from fastapi import APIRouter, Body
from fastapi.openapi.models import Example

from source.app.book_api.common.model import PaginationRequest, PaginationResponse
from source.app.book_api.dependency_injector import dependency_injector
from source.core.book.port.book_service import GetBooksBySubjectSpec, IBookService
from source.core.common.enum import BookSubject
from source.core.common.model import Book

router = APIRouter(prefix="/book", tags=["Book API"])
book_service: IBookService = dependency_injector.get(
    interface=IBookService  # type:ignore
)


class GetBooksBySubjectRequest(PaginationRequest):
    subject: BookSubject


class GetBooksBySubjectResponse(PaginationResponse):
    results: List[Book]


get_books_by_subject_body_examples = {
    BookSubject.MATHEMATICS.name: Example(
        summary=BookSubject.MATHEMATICS,
        description=f"Get books by {BookSubject.MATHEMATICS} subject",
        value={"subject": BookSubject.MATHEMATICS, "page": 1, "limit": 5},
    ),
    BookSubject.PHYSICS.name: Example(
        summary=BookSubject.PHYSICS,
        description=f"Get books by {BookSubject.PHYSICS} subject",
        value={"subject": BookSubject.PHYSICS, "page": 1, "limit": 5},
    ),
    BookSubject.PROGRAMMING.name: Example(
        summary=BookSubject.PROGRAMMING,
        description=f"Get books by {BookSubject.PROGRAMMING} subject",
        value={"subject": BookSubject.PROGRAMMING, "page": 1, "limit": 5},
    ),
}


@router.post("/get-by-subject", response_model=GetBooksBySubjectResponse)
def get_books_by_subject(
    request_data: GetBooksBySubjectRequest = Body(
        ..., openapi_examples=get_books_by_subject_body_examples
    )
):
    return book_service.get_books_by_subject(
        spec=GetBooksBySubjectSpec(**request_data.model_dump())
    )
