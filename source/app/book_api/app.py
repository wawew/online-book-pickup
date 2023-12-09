import logging
import os

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse

from source.app.book_api.api import book_api, user_api
from source.app.book_api.common.model import DEFAULT_API_RESPONSES
from source.core.common.exception import (
    EntityNotFoundException,
    ExpiredTokenException,
    GenericException,
    InvalidTokenException,
)

app = FastAPI(
    title="Online Book Pickup API",
    description="Onnline book pickup service",
    version="1.0.0",
    openapi_url=None if os.environ.get("APP_ENV") == "prod" else "/openapi.json",
    docs_url=None,
    responses=DEFAULT_API_RESPONSES,  # type: ignore
)
app.include_router(user_api.router)
app.include_router(book_api.router)


@app.get("/docs", include_in_schema=False)
def override_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title)  # type: ignore


@app.exception_handler(RequestValidationError)
def request_validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error_code": "API_VALIDATION_ERROR",
            "message": "Validation error",
            "payload": jsonable_encoder(exc.errors()),
        },
    )


exception_to_error_map = {
    GenericException: (422, "GENERIC_ERROR"),
    EntityNotFoundException: (422, "ENTITY_NOT_FOUND"),
    InvalidTokenException: (401, "INVALID_TOKEN_ERROR"),
    ExpiredTokenException: (401, "EXPIRED_TOKEN_ERROR"),
}


@app.middleware("http")
async def exception_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        if type(exc) not in exception_to_error_map:
            logging.exception("Unexpected error")
            return JSONResponse(
                status_code=500,
                content={
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "message": str(exc),
                },
            )

        status_code, error_code = exception_to_error_map[type(exc)]  # type: ignore
        return JSONResponse(
            status_code=status_code,
            content={
                "error_code": error_code,
                "message": str(exc),
                "payload": getattr(exc, "payload", None),
            },
        )
