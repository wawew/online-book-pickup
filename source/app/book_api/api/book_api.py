from datetime import datetime
from typing import List

from fastapi import APIRouter, Body, Depends
from fastapi.openapi.models import Example

from source.app.book_api.authorizer import authorize_request
from source.app.book_api.common.model import (
    PaginationRequest,
    PaginationResponse,
    PydanticBaseModel,
)
from source.app.book_api.dependency_injector import dependency_injector
from source.core.book.port.book_reservation_service import (
    GetAllBookReservationsSpec,
    IBookReservationService,
    ReserveBookSpec,
)
from source.core.book.port.book_service import GetBooksBySubjectSpec, IBookService
from source.core.common.enum import BookSubject, UserType
from source.core.common.model import Book, BookReservation

router = APIRouter(prefix="/book", tags=["Book API"])
book_service: IBookService = dependency_injector.get(
    interface=IBookService  # type:ignore
)
book_reservation_service: IBookReservationService = dependency_injector.get(
    interface=IBookReservationService  # type:ignore
)


class GetBooksBySubjectRequest(PaginationRequest):
    subject: BookSubject


class GetBooksBySubjectResponse(PaginationResponse):
    results: List[Book]


get_books_by_subject_body_examples = {
    BookSubject.MATHEMATICS.name: Example(
        summary=BookSubject.MATHEMATICS,
        description=f"Get books by {BookSubject.MATHEMATICS} subject",
        value={"subject": BookSubject.MATHEMATICS, "page": 1, "limit": 20},
    ),
    BookSubject.PHYSICS.name: Example(
        summary=BookSubject.PHYSICS,
        description=f"Get books by {BookSubject.PHYSICS} subject",
        value={"subject": BookSubject.PHYSICS, "page": 1, "limit": 20},
    ),
    BookSubject.PROGRAMMING.name: Example(
        summary=BookSubject.PROGRAMMING,
        description=f"Get books by {BookSubject.PROGRAMMING} subject",
        value={"subject": BookSubject.PROGRAMMING, "page": 1, "limit": 20},
    ),
}


@router.post(
    "/get-by-subject",
    response_model=GetBooksBySubjectResponse,
    dependencies=[Depends(authorize_request(UserType.MEMBER))],
)
def get_books_by_subject(
    request_data: GetBooksBySubjectRequest = Body(
        ..., openapi_examples=get_books_by_subject_body_examples
    )
):
    return book_service.get_books_by_subject(
        spec=GetBooksBySubjectSpec(**request_data.model_dump())
    )


class CreateBookReservationRequest(PydanticBaseModel):
    edition_key: str
    pickup_time: datetime
    reservation_start_time: datetime
    reservation_end_time: datetime


class CreateBookReservationResponse(PydanticBaseModel, BookReservation):
    pass


@router.post("/reservation/create", response_model=CreateBookReservationResponse)
def create_book_reservation(
    request_data: CreateBookReservationRequest,
    user_email: str = Depends(authorize_request(UserType.MEMBER)),
):
    return book_reservation_service.reserve_book(
        spec=ReserveBookSpec(**dict(request_data.model_dump(), user_email=user_email))
    )


class GetAllBookReservationsRequest(PaginationRequest):
    pass


class GetAllBookReservationsResponse(PaginationResponse):
    results: List[BookReservation]


@router.post(
    "/reservation/get-all",
    response_model=GetAllBookReservationsResponse,
    dependencies=[Depends(authorize_request(UserType.LIBRARIAN))],
)
def get_all_book_reservations(request_data: GetAllBookReservationsRequest):
    return book_reservation_service.get_all_book_reservations(
        spec=GetAllBookReservationsSpec(**request_data.model_dump())
    )
