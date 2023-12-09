from typing import Any, Dict

from injector import inject
from jwt import ExpiredSignatureError, decode, encode

from source.core.auth.port.token_adapter import ITokenAdapter
from source.core.common.exception import ExpiredTokenException, InvalidTokenException
from source.core.common.port.secret_adapter import ISecretAdapter, SecretEnum


class JWTAdapter(ITokenAdapter):
    __algorithm = "HS256"

    @inject
    def __init__(self, secret_adapter: ISecretAdapter) -> None:
        self.secret_adapter = secret_adapter

    def generate_token(self, payload: Dict[Any, Any]) -> str:
        token = encode(
            payload=payload,
            key=self.secret_adapter.get_secret(SecretEnum.JWT_SECRET_KEY),
            algorithm=self.__algorithm,
        )
        return token

    def verify_token(self, token: str) -> Dict[Any, Any]:
        try:
            return decode(
                jwt=token,
                key=self.secret_adapter.get_secret(SecretEnum.JWT_SECRET_KEY),
                algorithms=[self.__algorithm],
                verify=True,
            )
        except ExpiredSignatureError:
            raise ExpiredTokenException
        except Exception:
            raise InvalidTokenException
