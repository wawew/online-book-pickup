from typing import Any


class GenericException(Exception):
    pass


class BaseEntityException(GenericException):
    def __init__(self, entity: str, entity_id: Any, entity_id_name: str = "id"):
        self.entity = entity
        self.entity_id = entity_id
        self.entity_id_name = entity_id_name


class EntityNotFoundException(BaseEntityException):
    def __str__(self) -> str:
        return f"{self.entity} with {self.entity_id_name} {self.entity_id} is not found"


class ExpiredTokenException(GenericException):
    pass


class InvalidTokenException(GenericException):
    pass
