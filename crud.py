from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import Sweet, User
from schemas import SweetCreate, UserCreate

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


def create_sweet(db: Session, sweet_in: SweetCreate, owner_id: int) -> Sweet:
    """Persist a sweet to the database for the given payload.

    Args:
        db: Active SQLAlchemy session.
        sweet_in: Validated sweet payload provided by the client.
        owner_id: Identifier of the user creating the sweet.

    Returns:
        The newly created sweet record.
    """

    sweet = Sweet(
        name=sweet_in.name,
        category=sweet_in.category,
        price=sweet_in.price,
        quantity=sweet_in.quantity,
        owner_id=owner_id,
    )
    db.add(sweet)
    db.commit()
    db.refresh(sweet)
    return sweet


def get_sweets(db: Session, skip: int = 0, limit: int = 100, owner_id: int | None = None) -> list[Sweet]:
    """Retrieve sweets from the database with optional pagination controls.

    Args:
        db: Active SQLAlchemy session.
        skip: Number of records to skip from the beginning of the result set.
        limit: Maximum number of records to return.
        owner_id: Optional user identifier to filter sweets by owner.

    Returns:
        A list of sweets ordered by insertion sequence.
    """

    query = db.query(Sweet)
    if owner_id is not None:
        query = query.filter(Sweet.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()
