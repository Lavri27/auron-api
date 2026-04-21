from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def register(db: Session, payload: UserCreate) -> User:
        existing_email = db.query(User).filter(User.email == payload.email).first()
        if existing_email:
            raise ValueError("Email already registered")

        existing_username = db.query(User).filter(User.username == payload.username).first()
        if existing_username:
            raise ValueError("Username already taken")

        user = User(
            email=payload.email,
            username=payload.username,
            password_hash=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> tuple[str, str]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(str(user.id))
        refresh_token, expires_at = create_refresh_token(str(user.id))

        db.add(
            RefreshToken(
                user_id=user.id,
                token_hash=hash_token(refresh_token),
                expires_at=expires_at.replace(tzinfo=None),
            )
        )
        db.commit()

        return access_token, refresh_token

    @staticmethod
    def refresh(db: Session, raw_refresh_token: str) -> tuple[str, str]:
        payload = decode_token(raw_refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = int(payload.get("sub"))
        token_hash_value = hash_token(raw_refresh_token)

        stored = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash_value,
                RefreshToken.revoked_at.is_(None),
            )
            .first()
        )
        if not stored:
            raise ValueError("Refresh token not found or revoked")

        if stored.expires_at < datetime.utcnow():
            raise ValueError("Refresh token expired")

        stored.revoked_at = datetime.utcnow()

        new_access_token = create_access_token(str(user_id))
        new_refresh_token, expires_at = create_refresh_token(str(user_id))

        db.add(
            RefreshToken(
                user_id=user_id,
                token_hash=hash_token(new_refresh_token),
                expires_at=expires_at.replace(tzinfo=None),
            )
        )
        db.commit()

        return new_access_token, new_refresh_token

    @staticmethod
    def logout(db: Session, raw_refresh_token: str) -> None:
        token_hash_value = hash_token(raw_refresh_token)
        stored = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash_value,
                RefreshToken.revoked_at.is_(None),
            )
            .first()
        )
        if stored:
            stored.revoked_at = datetime.utcnow()
            db.commit()
