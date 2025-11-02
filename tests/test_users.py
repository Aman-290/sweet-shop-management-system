def test_read_current_user_success(client) -> None:
    email = "test@example.com"
    password = "password123"

    register_payload = {"email": email, "password": password}
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 201

    login_payload = {"username": email, "password": password}
    login_response = client.post("/api/auth/login", data=login_payload)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body.get("email") == email
