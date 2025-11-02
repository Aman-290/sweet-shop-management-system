from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

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
		user = crud.create_user(db, user_in, role=user_in.role)
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


@app.get("/api/auth/me", response_model=schemas.UserOut)
def get_current_user_info(
	current_user: models.User = Depends(security.get_current_user),
) -> models.User:
	"""Retrieve the authenticated user's information.

	Args:
		current_user: The authenticated user from the token.

	Returns:
		The user model with id, email, and role.
	"""
	return current_user


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
	current_user: models.User = Depends(security.require_admin),
) -> models.Sweet:
	"""Persist a new sweet and associate it with the authenticated user.
	
	Admin access required.

	Args:
		sweet_in: Validated payload describing the sweet to create.
		db: Database session injected by FastAPI.
		current_user: The authenticated admin user initiating the request.

	Returns:
		The persisted sweet model serialized via response schema.
	"""

	return crud.create_sweet(db, sweet_in, owner_id=current_user.id)


@app.get("/api/sweets", response_model=list[schemas.Sweet])
def list_sweets(
	skip: int = 0,
	limit: int = 100,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.get_current_user),
) -> list[models.Sweet]:
	"""Return sweets visible to the authenticated user with optional pagination.

	Args:
		skip: Number of records to omit from the start of the result set.
		limit: Maximum number of sweets to return.
		db: Database session supplied by FastAPI's dependency injection.
		current_user: The authenticated user initiating the request.

	Returns:
		A list of sweets persisted in the system.
	"""

	return crud.get_sweets(db, skip=skip, limit=limit, owner_id=current_user.id)


@app.get("/api/sweets/search", response_model=list[schemas.Sweet])
def search_sweets(
	name: str | None = None,
	category: str | None = None,
	min_price: float | None = None,
	max_price: float | None = None,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.get_current_user),
) -> list[models.Sweet]:
	"""Search sweets using optional filters for name, category, or price range.

	Args:
		name: Optional name fragment to match (case-insensitive).
		category: Optional category to filter by.
		min_price: Optional lower bound for the sweet price.
		max_price: Optional upper bound for the sweet price.
		db: Database session injected via dependency.
		current_user: The authenticated user initiating the request.

	Returns:
		A list of sweets that satisfy the supplied filters.
	"""

	return crud.search_sweets(
		db,
		name=name,
		category=category,
		min_price=min_price,
		max_price=max_price,
		owner_id=current_user.id,
	)


@app.put("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def update_sweet(
	sweet_id: int,
	sweet_update: schemas.SweetUpdate,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.require_admin),
) -> schemas.Sweet:
	"""Update an existing sweet belonging to the authenticated user.
	
	Admin access required.

	Args:
		sweet_id: Identifier of the sweet to modify.
		sweet_update: Payload specifying fields and values to update.
		db: Database session injected by FastAPI.
		current_user: The authenticated admin user performing the update.

	Returns:
		The updated sweet serialized via the response schema.

	Raises:
		HTTPException: If the sweet does not exist or is not owned by the user.
	"""

	sweet = crud.get_sweet(db, sweet_id)
	if sweet is None or sweet.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sweet not found")

	updated = crud.update_sweet(db, sweet_id, sweet_update)
	assert updated is not None
	return updated


@app.delete("/api/sweets/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sweet(
	sweet_id: int,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.require_admin),
) -> None:
	"""Delete a sweet owned by the authenticated user.
	
	Admin access required.

	Args:
		sweet_id: Identifier of the sweet to remove.
		db: Database session injected by FastAPI.
		current_user: The authenticated admin user performing the deletion.

	Raises:
		HTTPException: If the sweet does not exist or is not owned by the user.
	"""

	sweet = crud.get_sweet(db, sweet_id)
	if sweet is None or sweet.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sweet not found")

	crud.delete_sweet(db, sweet_id)


@app.get("/api/sweets/{sweet_id}", response_model=schemas.Sweet)
def get_sweet(
	sweet_id: int,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.get_current_user),
) -> schemas.Sweet:
	"""Retrieve a sweet owned by the authenticated user.

	Args:
		sweet_id: Identifier of the sweet to fetch.
		db: Database session supplied by FastAPI.
		current_user: The authenticated user requesting the sweet.

	Returns:
		The sweet model serialized via response schema.

	Raises:
		HTTPException: If the sweet does not exist or is not owned by the user.
	"""

	sweet = crud.get_sweet(db, sweet_id)
	if sweet is None or sweet.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sweet not found")

	return sweet


@app.post("/api/sweets/{sweet_id}/purchase", response_model=schemas.Sweet)
def purchase_sweet(
	sweet_id: int,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.get_current_user),
) -> schemas.Sweet:
	"""Purchase a sweet by reducing its quantity by one.

	Args:
		sweet_id: Identifier of the sweet to purchase.
		db: Database session provided by FastAPI.
		current_user: The authenticated user executing the purchase.

	Returns:
		The updated sweet model after the purchase.

	Raises:
		HTTPException: If the sweet is not found or if it is out of stock.
	"""

	sweet = crud.get_sweet(db, sweet_id)
	if sweet is None or sweet.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sweet not found")

	result = crud.purchase_sweet(db, sweet_id)
	if result is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sweet not found")
	if result == "out_of_stock":
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sweet is out of stock")

	return result


@app.post("/api/sweets/{sweet_id}/restock", response_model=schemas.Sweet)
def restock_sweet(
	sweet_id: int,
	restock_request: schemas.RestockRequest,
	db: Session = Depends(get_db),
	current_user: models.User = Depends(security.require_admin),
) -> schemas.Sweet:
	"""Restock a sweet owned by the authenticated user.
	
	Admin access required.

	Args:
		sweet_id: Identifier of the sweet to restock.
		restock_request: Payload containing the quantity to add.
		db: Database session injected by FastAPI.
		current_user: The authenticated admin user performing the restock.

	Returns:
		The updated sweet model serialized via response schema.

	Raises:
		HTTPException: If the sweet does not exist or is not owned by the user.
	"""

	sweet = crud.get_sweet(db, sweet_id)
	if sweet is None or sweet.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sweet not found")

	updated = crud.restock_sweet(db, sweet_id, restock_request.quantity)
	if updated is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sweet not found")

	return updated
