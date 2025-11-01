from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import User
from schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str) -> User | None:
    """Fetch a single user matching the supplied email address.

    Args:
        db: Active SQLAlchemy session.
        email: Email address to search for.

    Returns:
        The matching user record if one exists; otherwise None.
    """

    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """Persist a new user in the database.

    Args:
        db: Active SQLAlchemy session.
        user_in: Validated payload containing email and password.

    Returns:
        The newly created user record.

    Raises:
        ValueError: If the email is already associated with an existing user.
    """

    if get_user_by_email(db, user_in.email) is not None:
        raise ValueError("Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=_hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
