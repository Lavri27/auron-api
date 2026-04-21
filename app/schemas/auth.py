from pydantic import EmailStr

from app.schemas.common import ORMModel


class LoginRequest(ORMModel):
    email: EmailStr
    password: str


class TokenResponse(ORMModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(ORMModel):
    refresh_token: str


class LogoutRequest(ORMModel):
    refresh_token: str
