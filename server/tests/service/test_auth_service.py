import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from server.services.auth_service import AuthService
from server.schemas.schema import UserRegistrationRequest, UserLoginRequest
from server.models.model import User, UserType


@pytest.fixture(autouse=True)
def _cleanup_users(db_session):
    """Ensure users table is cleaned between tests since we commit in tests."""
    try:
        yield
    finally:
        try:
            db_session.rollback()
        except Exception:
            pass
        db_session.query(User).delete()
        db_session.commit()


def _count_users(db_session) -> int:
    return db_session.query(User).count()


def _get_user_by_email(db_session, email: str):
    return db_session.query(User).filter(User.email == email).first()


# -------------------- register_user --------------------

def test_register_user_success_tenant(db_session, monkeypatch):
    # Arrange: mock hashing to deterministic value
    monkeypatch.setattr("server.services.auth_service.get_password_hash", lambda pw: f"hash:{pw}")

    req = UserRegistrationRequest(
        name="Alice",
        email="alice@example.com",
        phone="1234567890",
        password="secret",
        user_type="tenant",
    )

    # Act
    resp = AuthService.register_user(req, db_session)

    # Assert
    assert resp.id > 0
    assert resp.name == "Alice"
    assert resp.email == "alice@example.com"
    assert resp.user_type == "tenant"
    # persisted row
    u = _get_user_by_email(db_session, "alice@example.com")
    assert u is not None
    assert u.user_type == UserType.TENANT
    assert u.password_hash == "hash:secret"


def test_register_user_success_owner(db_session, monkeypatch):
    monkeypatch.setattr("server.services.auth_service.get_password_hash", lambda pw: "fixed-hash")
    req = UserRegistrationRequest(
        name="Bob",
        email="bob@example.com",
        phone="1112223333",
        password="pw",
        user_type="owner",
    )

    resp = AuthService.register_user(req, db_session)

    assert resp.user_type == "owner"
    u = _get_user_by_email(db_session, "bob@example.com")
    assert u.user_type == UserType.OWNER
    assert u.password_hash == "fixed-hash"


def test_register_user_duplicate_precheck_returns_400(db_session, monkeypatch):
    # Pre-insert a user with same email so pre-check triggers
    u = User(
        name="X",
        email="dup@example.com",
        phone="0",
        password_hash="h",
        user_type=UserType.OWNER,
    )
    db_session.add(u)
    db_session.commit()

    req = UserRegistrationRequest(
        name="X",
        email="dup@example.com",
        phone="0",
        password="pw",
        user_type="tenant",
    )

    with pytest.raises(HTTPException) as ei:
        AuthService.register_user(req, db_session)
    err = ei.value
    assert err.status_code == 400
    assert "already exists" in err.detail


def test_register_user_integrity_error_raised_during_commit_returns_400(db_session, monkeypatch):
    # Ensure no existing user so we reach commit path
    req = UserRegistrationRequest(
        name="Y",
        email="race@example.com",
        phone="0",
        password="pw",
        user_type="tenant",
    )

    # Mock hashing to avoid external deps
    monkeypatch.setattr("server.services.auth_service.get_password_hash", lambda pw: "h")

    # Patch commit to raise IntegrityError (simulate race condition unique violation)
    original_commit = db_session.commit

    def raise_integrity():
        raise IntegrityError("stmt", params=None, orig=Exception("unique"))

    try:
        db_session.commit = raise_integrity  # type: ignore[assignment]
        with pytest.raises(HTTPException) as ei:
            AuthService.register_user(req, db_session)
        err = ei.value
        assert err.status_code == 400
        assert "already exists" in err.detail
    finally:
        db_session.rollback()
        db_session.commit = original_commit  # restore


def test_register_user_generic_exception_returns_500(db_session, monkeypatch):
    req = UserRegistrationRequest(
        name="Z",
        email="oops@example.com",
        phone="0",
        password="pw",
        user_type="owner",
    )
    monkeypatch.setattr("server.services.auth_service.get_password_hash", lambda pw: "h")

    original_commit = db_session.commit

    def raise_generic():
        raise RuntimeError("db down")

    try:
        db_session.commit = raise_generic  # type: ignore[assignment]
        with pytest.raises(HTTPException) as ei:
            AuthService.register_user(req, db_session)
        err = ei.value
        assert err.status_code == 500
        assert "Internal server error" in err.detail
    finally:
        db_session.rollback()
        db_session.commit = original_commit


# -------------------- login_user --------------------

def test_login_user_success_returns_token(db_session, monkeypatch):
    # Create a user with known password hash and mock verify + token
    u = User(
        name="L",
        email="login@example.com",
        phone="0",
        password_hash="hashed",
        user_type=UserType.OWNER,
    )
    db_session.add(u)
    db_session.commit()

    monkeypatch.setattr("server.services.auth_service.verify_password", lambda pw, ph: True)
    monkeypatch.setattr("server.services.auth_service.create_access_token", lambda data: "tok")

    req = UserLoginRequest(email="login@example.com", password="secret")
    res = AuthService.login_user(req, db_session)

    assert res["access_token"] == "tok"
    assert res["token_type"] == "bearer"


def test_login_user_incorrect_password_raises_401(db_session, monkeypatch):
    u = User(
        name="L2",
        email="wrongpw@example.com",
        phone="0",
        password_hash="hashed",
        user_type=UserType.TENANT,
    )
    db_session.add(u)
    db_session.commit()

    monkeypatch.setattr("server.services.auth_service.verify_password", lambda pw, ph: False)

    req = UserLoginRequest(email="wrongpw@example.com", password="bad")
    with pytest.raises(HTTPException) as ei:
        AuthService.login_user(req, db_session)
    err = ei.value
    assert err.status_code == 401
    assert "Incorrect email or password" in err.detail


def test_login_user_nonexistent_email_raises_401(db_session, monkeypatch):
    # No user created for this email
    monkeypatch.setattr("server.services.auth_service.verify_password", lambda pw, ph: False)

    req = UserLoginRequest(email="nosuch@example.com", password="x")
    with pytest.raises(HTTPException) as ei:
        AuthService.login_user(req, db_session)
    err = ei.value
    assert err.status_code == 401


# -------------------- read helpers --------------------

def test_get_all_users_and_get_user_by_email(db_session):
    u1 = User(name="A", email="a@example.com", phone="1", password_hash="h", user_type=UserType.OWNER)
    u2 = User(name="B", email="b@example.com", phone="2", password_hash="h", user_type=UserType.TENANT)
    db_session.add_all([u1, u2])
    db_session.commit()

    users = AuthService.get_all_users(db_session)
    emails = sorted([u.email for u in users])
    assert emails == ["a@example.com", "b@example.com"]

    u = AuthService.get_user_by_email("b@example.com", db_session)
    assert u is not None
    assert u.email == "b@example.com"
