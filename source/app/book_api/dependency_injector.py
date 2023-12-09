from injector import Injector

from source.app.book_api.module import ApplicationModule
from source.infra.auth.module import AuthAdapterModule
from source.infra.book.module import BookAdapterModule

dependency_injector = Injector(
    [ApplicationModule, AuthAdapterModule, BookAdapterModule]
)
