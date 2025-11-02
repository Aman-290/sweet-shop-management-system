import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Use test database
TEST_DATABASE_URL = "sqlite:///./test_sweetshop.db"

# Import after path is set
from database import Base, get_db
from main import app
import models

# Create test engine
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database before tests, clean up after."""
    # Remove existing test database
    test_db = Path("test_sweetshop.db")
    if test_db.exists():
        test_db.unlink()

    # Create tables
    Base.metadata.create_all(bind=engine)

    yield

    # Cleanup after all tests
    Base.metadata.drop_all(bind=engine)
    engine.dispose()  # Close all connections
    import time
    time.sleep(0.1)  # Give Windows a moment to release file handles
    if test_db.exists():
        try:
            test_db.unlink()
        except PermissionError:
            pass  # Database file still locked, will be cleaned on next run

@pytest.fixture(scope="function")
def client():
    """Provide a test client for each test."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    """Reset database before each test."""
    # Clear all data but keep tables
    db = TestingSessionLocal()
    try:
        db.query(models.Sweet).delete()
        db.query(models.User).delete()
        db.commit()
    finally:
        db.close()
