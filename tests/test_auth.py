def test_register_user_success(client) -> None:
    payload = {"email": "register@example.com", "password": "password123"}
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert data["email"] == "register@example.com"
    assert "role" in data
    assert data["role"] == "customer"  # Default role


def test_login_user_success(client) -> None:
    registration_payload = {"email": "login@example.com", "password": "password123"}
    register_response = client.post("/api/auth/register", json=registration_payload)
    assert register_response.status_code == 201

    login_payload = {"username": "login@example.com", "password": "password123"}
    response = client.post("/api/auth/login", data=login_payload)

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body.get("token_type") == "bearer"
