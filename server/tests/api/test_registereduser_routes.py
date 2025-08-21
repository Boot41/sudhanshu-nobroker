import pytest
from fastapi.testclient import TestClient

from server.models.model import User, UserType
from server.core.security import get_password_hash
from server.api import dependencies as api_deps


@pytest.fixture(autouse=True)
def _cleanup_users(db_session):
    yield
    db_session.query(User).delete()
    db_session.commit()


def _mk_user(db, email: str, user_type: UserType) -> User:
    u = User(
        name="User",
        email=email,
        phone="1234567890",
        password_hash=get_password_hash("pass"),
        user_type=user_type,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _override_current_user(app, user: User):
    app.dependency_overrides[api_deps.get_current_user] = lambda: user


def _clear_current_user_override(app):
    app.dependency_overrides.pop(api_deps.get_current_user, None)


def test_get_my_profile_owner(client: TestClient, db_session):
    app = client.app
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    _override_current_user(app, owner)

    r = client.get("/users/me")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == owner.id
    assert data["email"] == owner.email
    assert data["user_type"] == UserType.OWNER.value
    assert "created_at" in data


def test_get_my_profile_tenant(client: TestClient, db_session):
    app = client.app
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)
    _override_current_user(app, tenant)

    r = client.get("/users/me")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == tenant.id
    assert data["user_type"] == UserType.TENANT.value


def test_update_my_profile_partial_name(client: TestClient, db_session):
    app = client.app
    user = _mk_user(db_session, "u@example.com", UserType.TENANT)
    _override_current_user(app, user)

    r = client.put("/users/me", json={"name": "New Name"})
    assert r.status_code == 200
    assert r.json()["name"] == "New Name"


def test_update_my_profile_partial_phone(client: TestClient, db_session):
    app = client.app
    user = _mk_user(db_session, "u2@example.com", UserType.OWNER)
    _override_current_user(app, user)

    r = client.put("/users/me", json={"phone": "0000000000"})
    assert r.status_code == 200
    assert r.json()["phone"] == "0000000000"


def test_update_my_profile_both_fields(client: TestClient, db_session):
    app = client.app
    user = _mk_user(db_session, "u3@example.com", UserType.TENANT)
    _override_current_user(app, user)

    r = client.put("/users/me", json={"name": "Combo", "phone": "1111111111"})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Combo"
    assert body["phone"] == "1111111111"


def test_update_my_profile_noop(client: TestClient, db_session):
    app = client.app
    user = _mk_user(db_session, "u4@example.com", UserType.OWNER)
    _override_current_user(app, user)

    r = client.put("/users/me", json={})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == user.name
    assert body["phone"] == user.phone


def test_update_my_profile_empty_strings_allowed(client: TestClient, db_session):
    app = client.app
    user = _mk_user(db_session, "u5@example.com", UserType.TENANT)
    _override_current_user(app, user)

    r = client.put("/users/me", json={"name": "", "phone": ""})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == ""
    assert body["phone"] == ""


def test_me_requires_auth_when_no_override(client: TestClient):
    # Remove current_user override to exercise dependency behavior
    app = client.app
    _clear_current_user_override(app)

    r = client.get("/users/me")
    # HTTPBearer returns 403 when no Authorization header is provided
    assert r.status_code == 403
    assert r.json().get("detail") == "Not authenticated"
