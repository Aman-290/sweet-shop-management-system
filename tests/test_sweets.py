from uuid import uuid4


def test_create_sweet_success(client) -> None:
    email = f"sweet_tester_{uuid4().hex}@example.com"
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


def test_get_all_sweets_success(client) -> None:
    email = f"sweet_list_tester_{uuid4().hex}@example.com"
    password = "password123"

    register_payload = {"email": email, "password": password, "role": "admin"}
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


def test_search_sweets_by_name(client) -> None:
    email = f"sweet_search_{uuid4().hex}@example.com"
    password = "password123"

    register_payload = {"email": email, "password": password, "role": "admin"}
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_payload = {"username": email, "password": password}
    login_response = client.post("/api/auth/login", data=login_payload)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    sweets = [
        {"name": "Chocolate Eclair", "category": "Pastry", "price": 2.50, "quantity": 10},
        {"name": "Caramel Tart", "category": "Pastry", "price": 3.00, "quantity": 8},
        {"name": "Chocolate Mousse", "category": "Dessert", "price": 4.25, "quantity": 6},
    ]

    for payload in sweets:
        response = client.post("/api/sweets", json=payload, headers=headers)
        assert response.status_code == 201

    response = client.get("/api/sweets/search", params={"name": "Chocolate"}, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_update_sweet_success(client) -> None:
    email = f"sweet_update_{uuid4().hex}@example.com"
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
        "name": "Lemon Tart",
        "category": "Dessert",
        "price": 2.75,
        "quantity": 7,
    }

    create_response = client.post("/api/sweets", json=sweet_payload, headers=headers)
    assert create_response.status_code == 201
    sweet_id = create_response.json()["id"]

    update_payload = {"price": 3.00, "quantity": 5}

    response = client.put(f"/api/sweets/{sweet_id}", json=update_payload, headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["price"] == 3.00
    assert body["quantity"] == 5


def test_delete_sweet_success(client) -> None:
    email = f"sweet_delete_{uuid4().hex}@example.com"
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
        "name": "Pistachio Macaron",
        "category": "Dessert",
        "price": 3.50,
        "quantity": 4,
    }

    create_response = client.post("/api/sweets", json=sweet_payload, headers=headers)
    assert create_response.status_code == 201
    sweet_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/sweets/{sweet_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/sweets/{sweet_id}", headers=headers)
    assert get_response.status_code == 404
