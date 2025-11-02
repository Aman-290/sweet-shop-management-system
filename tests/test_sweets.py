import sys
from pathlib import Path
from uuid import uuid4

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_sweet_success() -> None:
    email = f"sweet_tester_{uuid4().hex}@example.com"
    password = "password123"

    register_payload = {"email": email, "password": password}
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_payload = {"username": email, "password": password}
    login_response = client.post("/api/auth/login", data=login_payload)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    sweet_payload = {
        "name": "Chocolate Eclair",
        "category": "Pastry",
        "price": 2.50,
        "quantity": 10,
    }

    response = client.post("/api/sweets", json=sweet_payload, headers=headers)

    assert response.status_code == 201
    body = response.json()
    assert body.get("name") == sweet_payload["name"]
    assert body.get("category") == sweet_payload["category"]
