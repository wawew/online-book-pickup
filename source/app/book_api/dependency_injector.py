from injector import Injector

from source.app.book_api.module import ApplicationModule
from source.infra.auth.module import AuthAdapterModule

dependency_injector = Injector([ApplicationModule, AuthAdapterModule])
