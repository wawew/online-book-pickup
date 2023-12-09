from typing import no_type_check

from injector import Binder, Module, singleton

from source.core.auth.port.token_adapter import ITokenAdapter
from source.core.auth.port.user_adapter import IUserAdapter
from source.infra.auth.adapter.token import JWTAdapter
from source.infra.auth.adapter.user import LocalStorageUserAdapter


class AuthAdapterModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        binder.bind(
            interface=IUserAdapter,
            to=LocalStorageUserAdapter,
            scope=singleton,
        )
        binder.bind(interface=ITokenAdapter, to=JWTAdapter, scope=singleton)
