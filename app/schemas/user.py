from datetime import datetime

from pydantic import EmailStr

from app.schemas.common import ORMModel


class UserCreate(ORMModel):
    email: EmailStr
    username: str
    password: str


class UserRead(ORMModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
