import sys

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def main():
    if len(sys.argv) < 4:
        print("Usage: python scripts/create_admin.py <email> <username> <password>")
        sys.exit(1)

    email = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    db = SessionLocal()
    try:
        existing = db.query(User).filter((User.email == email) | (User.username == username)).first()
        if existing:
            print("User with this email or username already exists")
            sys.exit(1)

        user = User(
            email=email,
            username=username,
            password_hash=hash_password(password),
            is_active=True,
            is_admin=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"Admin created: id={user.id}, email={user.email}, username={user.username}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
