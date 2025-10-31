from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_user_success() -> None:
    payload = {"email": "test@example.com", "password": "password123"}
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
