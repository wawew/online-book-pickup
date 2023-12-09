from datetime import datetime, timedelta, timezone

from injector import inject

from source.core.auth.port.authentication_service import (
    AuthenticateResult,
    AuthenticateSpec,
    IAuthenticationService,
)
from source.core.auth.port.token_adapter import ITokenAdapter
from source.core.auth.port.user_adapter import IUserAdapter
from source.core.common.enum import UserType
from source.core.common.exception import EntityNotFoundException, GenericException


class AuthenticationService(IAuthenticationService):
    @inject
    def __init__(
        self, user_adapter: IUserAdapter, token_adapter: ITokenAdapter
    ) -> None:
        self.user_adapter = user_adapter
        self.token_adapter = token_adapter

    def authenticate_librarian(self, spec: AuthenticateSpec) -> AuthenticateResult:
        return self.__authenticate(spec=spec, user_type=UserType.LIBRARIAN)

    def authenticate_member(self, spec: AuthenticateSpec) -> AuthenticateResult:
        return self.__authenticate(spec=spec, user_type=UserType.MEMBER)

    def __authenticate(
        self, spec: AuthenticateSpec, user_type: UserType
    ) -> AuthenticateResult:
        user = self.user_adapter.get_user_by_email(email=spec.email)
        if not user or user.user_type != user_type:
            raise EntityNotFoundException(
                entity="User", entity_id_name="email", entity_id=spec.email
            )

        credential = self.user_adapter.generate_credential(
            salt=user.salt, password=spec.password
        )
        if credential != user.credential:
            raise GenericException("Invalid email or password")

        token = self.token_adapter.generate_token(
            payload=dict(
                email=spec.email,
                exp=(datetime.now(tz=timezone.utc) + timedelta(hours=8)).timestamp(),
                user_type=user.user_type,
            )
        )
        return AuthenticateResult(email=spec.email, token=token)
