from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app

client = TestClient(app)


def test_register_login_verify_flow():
    # Use a unique email each run to avoid collisions with existing DB state
    email = f"testuser+{uuid4().hex}@example.com"
    password = "s3cret"

    # Register
    r = client.post("/register",
                    json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["email"] == email

    # Duplicate registration should fail
    r2 = client.post("/register",
                     json={"email": email, "password": password})
    assert r2.status_code == 400

    # Login (OAuth2 form)
    r3 = client.post("/token",
                     data={"username": email, "password": password})
    assert r3.status_code == 200, r3.text
    token = r3.json()["access_token"]
    assert token

    # Verify token should return X-User-ID header and body with user_id
    headers = {"Authorization": f"Bearer {token}"}
    r4 = client.get("/verify-token", headers=headers)
    assert r4.status_code == 200, r4.text
    # Header set by the endpoint
    assert "X-User-ID" in r4.headers
    body = r4.json()
    assert body.get("user_id") is not None

    # Test /me endpoint - should return current user profile
    r5 = client.get("/me", headers=headers)
    assert r5.status_code == 200, r5.text
    user_profile = r5.json()
    assert user_profile["email"] == email
    assert "id" in user_profile
