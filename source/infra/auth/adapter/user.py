import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional

from source.core.auth.port.user_adapter import IUserAdapter
from source.core.common.enum import UserStatus, UserType
from source.core.common.model import User


class LocalStorageUserAdapter(IUserAdapter):
    def __init__(self) -> None:
        self.__local_data = self.__initiate_local_data()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.__local_data.get(email)

    def generate_credential(self, salt: str, password: str) -> str:
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

    def __initiate_local_data(self) -> Dict[str, User]:
        return {
            "member@email.com": User(
                created_at=datetime.now(tz=timezone.utc),
                created_by="SYSTEM",
                email="member@email.com",
                user_type=UserType.MEMBER,
                status=UserStatus.ACTIVE,
                salt="123",
                credential=self.generate_credential(salt="123", password="member"),
                updated_at=None,
                updated_by=None,
            ),
            "librarian@email.com": User(
                created_at=datetime.now(tz=timezone.utc),
                created_by="SYSTEM",
                email="librarian@email.com",
                user_type=UserType.LIBRARIAN,
                status=UserStatus.ACTIVE,
                salt="123",
                credential=self.generate_credential(salt="123", password="librarian"),
                updated_at=None,
                updated_by=None,
            ),
        }
