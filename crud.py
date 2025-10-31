from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import User
from schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user_in: UserCreate) -> User:
    if db.query(User).filter(User.email == user_in.email).first() is not None:
        raise ValueError("Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=_hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
