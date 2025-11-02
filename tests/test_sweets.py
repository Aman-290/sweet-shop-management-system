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


def test_get_all_sweets_success() -> None:
    email = f"sweet_list_tester_{uuid4().hex}@example.com"
    password = "password123"

    register_payload = {"email": email, "password": password}
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_payload = {"username": email, "password": password}
    login_response = client.post("/api/auth/login", data=login_payload)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    sweet_one = {
        "name": "Vanilla Cupcake",
        "category": "Pastry",
        "price": 1.99,
        "quantity": 12,
    }
    sweet_two = {
        "name": "Strawberry Tart",
        "category": "Dessert",
        "price": 3.50,
        "quantity": 5,
    }

    first_response = client.post("/api/sweets", json=sweet_one, headers=headers)
    assert first_response.status_code == 201

    second_response = client.post("/api/sweets", json=sweet_two, headers=headers)
    assert second_response.status_code == 201

    response = client.get("/api/sweets", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == sweet_one["name"]
