from uuid import uuid4


def test_purchase_sweet_success(client) -> None:
    email = f"inventory_purchase_{uuid4().hex}@example.com"
    password = "password123"

    register_payload = {"email": email, "password": password, "role": "admin"}
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_payload = {"username": email, "password": password}
    login_response = client.post("/api/auth/login", data=login_payload)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    sweet_payload = {
        "name": "Mint Chocolate",
        "category": "Dessert",
        "price": 2.25,
        "quantity": 10,
    }

    create_response = client.post("/api/sweets", json=sweet_payload, headers=headers)
    assert create_response.status_code == 201
    sweet_id = create_response.json()["id"]

    response = client.post(f"/api/sweets/{sweet_id}/purchase", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["quantity"] == sweet_payload["quantity"] - 1


def test_restock_sweet_success(client) -> None:
    email = f"inventory_restock_{uuid4().hex}@example.com"
    password = "password123"

    register_payload = {"email": email, "password": password, "role": "admin"}
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_payload = {"username": email, "password": password}
    login_response = client.post("/api/auth/login", data=login_payload)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    initial_quantity = 10
    sweet_payload = {
        "name": "Hazelnut Praline",
        "category": "Dessert",
        "price": 3.75,
        "quantity": initial_quantity,
    }

    create_response = client.post("/api/sweets", json=sweet_payload, headers=headers)
    assert create_response.status_code == 201
    sweet_id = create_response.json()["id"]

    restock_payload = {"quantity": 50}

    response = client.post(
        f"/api/sweets/{sweet_id}/restock",
        json=restock_payload,
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["quantity"] == initial_quantity + restock_payload["quantity"]
