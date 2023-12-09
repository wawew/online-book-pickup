from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from source.core.common.enum import UserStatus, UserType


@dataclass
class BaseModel:
    created_at: datetime
    created_by: str
    updated_at: Optional[datetime]
    updated_by: Optional[str]


@dataclass
class User(BaseModel):
    email: str
    user_type: UserType
    status: UserStatus
    salt: str
    credential: str
