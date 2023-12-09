from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from pydantic import EmailStr

from source.app.book_api.common.model import PydanticBaseModel
from source.app.book_api.dependency_injector import dependency_injector
from source.core.auth.port.authentication_service import (
    AuthenticateSpec,
    IAuthenticationService,
)

router = APIRouter(prefix="/user", tags=["User API"])
auth_service: IAuthenticationService = dependency_injector.get(
    interface=IAuthenticationService  # type:ignore
)


class AuthenticateRequest(PydanticBaseModel):
    email: EmailStr
    password: str


class AuthenticateResponse(PydanticBaseModel):
    email: EmailStr
    token: str


authenticate_librarian_body_examples = {
    "librarian@email.com": Example(
        summary="librarian@email.com",
        value={"email": "librarian@email.com", "password": "librarian"},
    ),
}


@router.post("/authenticate-librarian", response_model=AuthenticateResponse)
def authenticate_librarian(
    auth_request: AuthenticateRequest = Body(
        ..., openapi_examples=authenticate_librarian_body_examples
    )
):
    return auth_service.authenticate_librarian(
        spec=AuthenticateSpec(**auth_request.model_dump())
    )


authenticate_member_body_examples = {
    "member@email.com": Example(
        summary="member@email.com",
        value={"email": "member@email.com", "password": "member"},
    ),
}


@router.post("/authenticate-member", response_model=AuthenticateResponse)
def authenticate_member(
    auth_request: AuthenticateRequest = Body(
        ..., openapi_examples=authenticate_member_body_examples
    )
):
    return auth_service.authenticate_member(
        spec=AuthenticateSpec(**auth_request.model_dump())
    )
