from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        token_type = payload.get("type")
        if token_type != "access":
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = db.get(User, user_id)
    if not user:
        raise credentials_exception

    return user


def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def get_current_author(user: User = Depends(get_current_user)) -> User:
    if not (user.is_author or user.is_admin):
        raise HTTPException(status_code=403, detail="Author access required")
    return user
