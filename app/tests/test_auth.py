from app.core.security import verify_password


def test_signup_and_login(client):
    # Signup
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "password": "secret123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["is_superuser"] is False
    assert data["is_active"] is True

    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_signup_existing_email(client):
    # First signup
    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "test@example.com",
            "password": "secret123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 400


def test_login_invalid_credentials(client):
    # Attempt login with invalid credentials
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400
