from abc import ABC, abstractmethod
from typing import Optional

from source.core.common.model import User


class IUserAdapter(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def generate_credential(self, salt: str, password: str) -> str:
        raise NotImplementedError
