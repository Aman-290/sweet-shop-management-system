from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "customer"  # Default to customer, can be overridden for testing


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: str


class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int


class Sweet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    price: float
    quantity: int
    owner_id: int


class SweetUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price: float | None = None
    quantity: int | None = None


class RestockRequest(BaseModel):
    """Payload for restocking a sweet by increasing its quantity."""

    quantity: int
