from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AuthenticateSpec:
    email: str
    password: str


@dataclass
class AuthenticateResult:
    email: str
    token: str


class IAuthenticationService(ABC):
    @abstractmethod
    def authenticate_librarian(self, spec: AuthenticateSpec) -> AuthenticateResult:
        raise NotImplementedError

    @abstractmethod
    def authenticate_member(self, spec: AuthenticateSpec) -> AuthenticateResult:
        raise NotImplementedError
