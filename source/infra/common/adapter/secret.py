import os

from dotenv import load_dotenv

from source.core.common.exception import GenericException
from source.core.common.port.secret_adapter import ISecretAdapter, SecretEnum


class LocalSecretAdapter(ISecretAdapter):
    def get_secret(self, key: SecretEnum) -> str:
        try:
            load_dotenv()
            return os.environ[key.value]
        except KeyError:
            raise GenericException
