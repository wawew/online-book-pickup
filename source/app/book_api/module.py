import os
from typing import no_type_check

from injector import Binder, Module, singleton

from source.core.auth.port.authentication_service import IAuthenticationService
from source.core.auth.service.authentication import AuthenticationService
from source.core.book.port.book_service import IBookService
from source.core.book.service.book import BookService
from source.core.common.port.secret_adapter import ISecretAdapter
from source.infra.common.adapter.secret import LocalSecretAdapter


class ApplicationModule(Module):
    @no_type_check
    def configure(self, binder: Binder) -> None:
        if os.getenv("APP_ENV") == "local":
            binder.bind(ISecretAdapter, to=LocalSecretAdapter, scope=singleton)

        binder.bind(IAuthenticationService, to=AuthenticationService, scope=singleton)
        binder.bind(IBookService, to=BookService, scope=singleton)
