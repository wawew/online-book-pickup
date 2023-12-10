from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from source.app.book_api.dependency_injector import dependency_injector
from source.core.auth.port.token_adapter import ITokenAdapter
from source.core.common.enum import UserType


class PermissionDenied(Exception):
    pass


def authorize_request(user_type: UserType):
    def authorizer(
        http_auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> str:
        token_adapter: ITokenAdapter = dependency_injector.get(
            ITokenAdapter  # type:ignore
        )
        token = http_auth.credentials
        payload_dict = token_adapter.verify_token(token)
        if payload_dict["user_type"] != user_type.name:
            raise PermissionDenied("Permission denied")
        return payload_dict["email"]

    return authorizer
