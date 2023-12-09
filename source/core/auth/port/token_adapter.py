from abc import ABC, abstractmethod
from typing import Any, Dict


class ITokenAdapter(ABC):
    @abstractmethod
    def generate_token(self, payload: Dict[Any, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str) -> Dict[Any, Any]:
        raise NotImplementedError
