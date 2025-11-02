from collections.abc import Generator
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Load environment variables
load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///./sweetshop.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    import models  # noqa: F401  # register models with metadata
    import crud
    import security

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create default admin user from environment variables
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    
    if admin_email and admin_password:
        db = SessionLocal()
        try:
            # Check if admin already exists
            existing_admin = crud.get_user_by_email(db, admin_email)
            if not existing_admin:
                # Create admin user
                hashed_password = security.get_password_hash(admin_password)
                admin_user = models.User(
                    email=admin_email,
                    hashed_password=hashed_password,
                    role="admin"
                )
                db.add(admin_user)
                db.commit()
                print(f"✅ Default admin created: {admin_email}")
            else:
                print(f"ℹ️  Admin already exists: {admin_email}")
        finally:
            db.close()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
