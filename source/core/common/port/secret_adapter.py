from abc import ABC, abstractmethod
from enum import Enum


class SecretEnum(Enum):
    JWT_SECRET_KEY = "JWT_SECRET_KEY"


class ISecretAdapter(ABC):
    @abstractmethod
    def get_secret(self, key: SecretEnum) -> str:
        raise NotImplementedError
