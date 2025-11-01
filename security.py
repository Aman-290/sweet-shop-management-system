from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import crud
import models
from database import get_db

SECRET_KEY = "change-this-secret-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Validate a plaintext password against a stored bcrypt hash.

    Args:
        plain_password: The candidate password provided by the user.
        hashed_password: The stored password hash for the user.

    Returns:
        True if the plaintext password matches the hash; otherwise False.
    """

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Generate a signed JWT access token for the supplied payload.

    Args:
        data: The claims to embed in the token payload.
        expires_delta: Optional override for the token lifetime.

    Returns:
        A JWT string signed with the application secret key.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
 ) -> models.User:
    """Resolve the authenticated user from the bearer token in the request.

    Args:
        token: The bearer token extracted from the Authorization header.
        db: SQLAlchemy session injected by FastAPI.

    Returns:
        The matching user model retrieved from the database.

    Raises:
        HTTPException: If the token is invalid, expired, or the user does not exist.
    """

    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc

    user = crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_error
    return user
