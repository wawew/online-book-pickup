from typing import Any

from pydantic import BaseModel


class PydanticBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
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
