import pytest
from fastapi import HTTPException

from server.core.security import get_password_hash
from server.models.model import User, UserType

# Uses fixtures from tests/conftest.py:
# - app (FastAPI)
# - client (TestClient) with dependency overrides for get_db and get_current_user
# - db_session (SQLAlchemy Session)


@pytest.fixture(autouse=True)
def _cleanup_users(db_session):
    """Ensure isolation for auth tests by cleaning users table after each test."""
    try:
        yield
    finally:
        try:
            db_session.rollback()
        except Exception:
            pass
        db_session.query(User).delete()
        db_session.commit()


def _mk_user(db_session, *, name="User", email="user@example.com", phone="0000000000", password="pass", user_type=UserType.OWNER) -> User:
    u = User(
        name=name,
        email=email,
        phone=phone,
        password_hash=get_password_hash(password),
        user_type=user_type,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


# -------------------- /auth/register --------------------

def test_register_tenant_success(client, db_session):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "1234567890",
        "password": "secret",
        "user_type": "tenant",
    }
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] > 0
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["phone"] == "1234567890"
    assert data["user_type"] == "tenant"
    assert data["message"] == "User registered successfully"
    assert "created_at" in data


def test_register_owner_success(client, db_session):
    payload = {
        "name": "Bob",
        "email": "bob@example.com",
        "phone": "1111111111",
        "password": "secret",
        "user_type": "owner",
    }
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["user_type"] == "owner"


def test_register_duplicate_email(client, db_session):
    _mk_user(db_session, email="dup@example.com")
    payload = {
        "name": "Dup",
        "email": "dup@example.com",
        "phone": "9999999999",
        "password": "secret",
        "user_type": "tenant",
    }
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 400
    assert r.json()["detail"] == "User with this email already exists"


def test_register_validation_invalid_email(client):
    payload = {
        "name": "X",
        "email": "not-an-email",
        "phone": "0",
        "password": "p",
        "user_type": "tenant",
    }
    r = client.post("/auth/register", json=payload)
    # Pydantic/FastAPI validation error
    assert r.status_code == 422


# -------------------- /auth/login --------------------

def test_login_success(client, db_session):
    _mk_user(db_session, email="u@example.com", password="pw123")
    r = client.post("/auth/login", json={"email": "u@example.com", "password": "pw123"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, db_session):
    _mk_user(db_session, email="u2@example.com", password="correct")
    r = client.post("/auth/login", json={"email": "u2@example.com", "password": "wrong"})
    assert r.status_code == 401
    body = r.json()
    assert body["detail"] == "Incorrect email or password"


def test_login_unknown_email(client):
    r = client.post("/auth/login", json={"email": "unknown@example.com", "password": "x"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Incorrect email or password"


# -------------------- /auth/logout --------------------

def test_logout_returns_message(client):
    # get_current_user is overridden by tests/conftest.py, so this is authenticated
    r = client.post("/auth/logout")
    assert r.status_code == 200
    assert r.json() == {"message": "Logged out"}
