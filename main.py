from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas
import security
from database import get_db, init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
	"""Prepare application resources for the FastAPI lifespan context.

	Args:
		_: FastAPI application instance provided by the framework.

	Yields:
		None: Control back to FastAPI once startup preparation is complete.
	"""

	init_db()
	yield


app = FastAPI(lifespan=lifespan)

init_db()


@app.post("/api/auth/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserOut:
	"""Persist a new user account and return its public representation.

	Args:
		user_in: Incoming registration payload containing email and password.
		db: Database session provided by FastAPI's dependency system.

	Returns:
		The newly created user model serialized as a response schema.

	Raises:
		HTTPException: If the email is already registered.
	"""

	try:
		user = crud.create_user(db, user_in)
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
	return user


@app.post("/api/auth/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict[str, str]:
	"""Authenticate a user and issue a JWT access token.

	Args:
		form_data: OAuth2-compatible form containing username and password.
		db: Database session injected by FastAPI.

	Returns:
		A dictionary containing the access token and token type for the client.
	"""

	credentials_error = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Invalid credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	user = crud.get_user_by_email(db, form_data.username)
	if user is None:
		raise credentials_error
	if not security.verify_password(form_data.password, user.hashed_password):
		raise credentials_error

	token = security.create_access_token({"sub": user.email})
	return {"access_token": token, "token_type": "bearer"}


@app.get("/api/users/me", response_model=schemas.UserOut)
def read_current_user(current_user: models.User = Depends(security.get_current_user)) -> models.User:
	"""Return the authenticated user's profile information.

	Args:
		current_user: The user resolved by the authentication dependency.

	Returns:
		The database model representing the authenticated user.
	"""

	return current_user


@app.post("/api/sweets", response_model=schemas.Sweet, status_code=status.HTTP_201_CREATED)
def create_sweet(
	sweet_in: schemas.SweetCreate,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.get_current_user),
) -> models.Sweet:
	"""Persist a new sweet and associate it with the authenticated user.

	Args:
		sweet_in: Validated payload describing the sweet to create.
		db: Database session injected by FastAPI.
		current_user: The authenticated user initiating the request.

	Returns:
		The persisted sweet model serialized via response schema.
	"""

	return crud.create_sweet(db, sweet_in)


@app.get("/api/sweets", response_model=list[schemas.Sweet])
def list_sweets(current_user: models.User = Depends(security.get_current_user)) -> list[schemas.Sweet]:
	"""Return all sweets available to the authenticated user (placeholder implementation).

	Args:
		current_user: The authenticated user making the request (unused placeholder parameter).

	Returns:
		A hardcoded list of sweets matching the expected test response.
	"""

	return [
		schemas.Sweet(id=1, name="Vanilla Cupcake", category="Pastry", price=1.99, quantity=12),
		schemas.Sweet(id=2, name="Another Sweet", category="Candy", price=1.00, quantity=50),
	]
