import sys
from pathlib import Path

db_file = Path("sweetshop.db")
if db_file.exists():
    db_file.unlink()

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_user_success() -> None:
    payload = {"email": "test@example.com", "password": "password123"}
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201


def test_login_user_success() -> None:
    registration_payload = {"email": "login@example.com", "password": "password123"}
    register_response = client.post("/api/auth/register", json=registration_payload)
    assert register_response.status_code == 201

    login_payload = {"username": "login@example.com", "password": "password123"}
    response = client.post("/api/auth/login", data=login_payload)

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body.get("token_type") == "bearer"
