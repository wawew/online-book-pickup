from typing import Any

from pydantic import BaseModel, PositiveInt


class PydanticBaseModel(BaseModel):
    class Config:
        populate_by_name = True
        extra = "ignore"


class DefaultErrorResponse(PydanticBaseModel):
    error_code: str
    message: str
    payload: Any


class DefaultSuccessResponse(PydanticBaseModel):
    message: str


DEFAULT_API_RESPONSES = {
    "200": {"model": DefaultSuccessResponse},
    "4XX": {"model": DefaultErrorResponse},
}


class PaginationRequest(PydanticBaseModel):
    page: PositiveInt
    limit: PositiveInt


class PaginationResponse(PaginationRequest):
    total: int
