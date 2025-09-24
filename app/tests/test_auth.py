import os
import sys
from pathlib import Path

# Ensure app package path is importable
THIS_DIR = Path(__file__).resolve().parent
APP_DIR = str(THIS_DIR.parent)
sys.path.insert(0, APP_DIR)

import json
import time
import pytest
from fastapi.testclient import TestClient

# Set test environment before importing the app so settings pick them up
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "testsecretkey")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "5")

from main import app  # import after env is set


client = TestClient(app)


def test_register_login_verify_flow():
    email = "testuser@example.com"
    password = "s3cret"

    # Register
    r = client.post("/api/user/register", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["email"] == email

    # Duplicate registration should fail
    r2 = client.post("/api/user/register", json={"email": email, "password": password})
    assert r2.status_code == 400

    # Login (OAuth2 form)
    r3 = client.post("/api/user/token", data={"username": email, "password": password})
    assert r3.status_code == 200, r3.text
    token = r3.json()["access_token"]
    assert token

    # Verify token should return X-User-ID header and body with user_id
    headers = {"Authorization": f"Bearer {token}"}
    r4 = client.get("/api/user/verify-token", headers=headers)
    assert r4.status_code == 200, r4.text
    # Header set by the endpoint
    assert "X-User-ID" in r4.headers
    body = r4.json()
    assert body.get("user_id") is not None
