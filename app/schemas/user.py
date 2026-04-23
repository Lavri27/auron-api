from datetime import datetime

from pydantic import EmailStr

from app.schemas.common import ORMModel


class UserCreate(ORMModel):
    email: EmailStr
    username: str
    password: str
    is_author: bool = False


class UserRead(ORMModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool
    is_author: bool
    created_at: datetime
