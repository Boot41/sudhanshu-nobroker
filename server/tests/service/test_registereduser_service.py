import pytest

from server.services.registereduser_service import RegisteredUserService
from server.models.model import User, UserType
from server.schemas.schema import UserMeUpdateRequest


# -------------------- fixtures & helpers --------------------

@pytest.fixture(autouse=True)
def _cleanup_users(db_session):
    """Ensure isolation: clean users table after each test.
    We delete in a FK-safe order if needed; this file only touches users though.
    """
    try:
        yield
    finally:
        try:
            db_session.rollback()
        except Exception:
            pass
        # In case other objects got created in future edits, keep it simple here
        db_session.query(User).delete()
        db_session.commit()


def _mk_user(db_session, *, name="User", email="user@example.com", phone="0000000000", user_type=UserType.OWNER) -> User:
    u = User(name=name, email=email, phone=phone, password_hash="hash", user_type=user_type)
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


# -------------------- tests: get_me --------------------

def test_get_me_returns_profile(db_session):
    user = _mk_user(db_session, name="Alice", email="alice@example.com", phone="1234567890", user_type=UserType.TENANT)

    resp = RegisteredUserService.get_me(db_session, user)

    assert resp.id == user.id
    assert resp.name == "Alice"
    assert resp.email == "alice@example.com"
    assert resp.phone == "1234567890"
    assert resp.user_type == user.user_type.value
    assert resp.created_at is not None


# -------------------- tests: update_me --------------------

def test_update_me_updates_name_and_phone_and_persists(db_session):
    user = _mk_user(db_session, name="Bob", email="bob@example.com", phone="1111111111", user_type=UserType.OWNER)

    payload = UserMeUpdateRequest(name="Bobby", phone="2222222222")
    resp = RegisteredUserService.update_me(db_session, user, payload)

    # response reflects updated values
    assert resp.name == "Bobby"
    assert resp.phone == "2222222222"

    # persisted to DB
    fetched = db_session.query(User).get(user.id)
    assert fetched.name == "Bobby"
    assert fetched.phone == "2222222222"

    # unchanged fields
    assert fetched.email == "bob@example.com"
    assert fetched.user_type == UserType.OWNER


def test_update_me_partial_only_name(db_session):
    user = _mk_user(db_session, name="Carol", email="carol@example.com", phone="3333333333", user_type=UserType.TENANT)

    payload = UserMeUpdateRequest(name="Caroline")
    resp = RegisteredUserService.update_me(db_session, user, payload)

    assert resp.name == "Caroline"
    assert resp.phone == "3333333333"  # unchanged

    fetched = db_session.query(User).get(user.id)
    assert fetched.name == "Caroline"
    assert fetched.phone == "3333333333"


def test_update_me_partial_only_phone(db_session):
    user = _mk_user(db_session, name="Dan", email="dan@example.com", phone="4444444444")

    payload = UserMeUpdateRequest(phone="5555555555")
    resp = RegisteredUserService.update_me(db_session, user, payload)

    assert resp.name == "Dan"  # unchanged
    assert resp.phone == "5555555555"

    fetched = db_session.query(User).get(user.id)
    assert fetched.name == "Dan"
    assert fetched.phone == "5555555555"


def test_update_me_no_fields_is_noop(db_session):
    user = _mk_user(db_session, name="Eve", email="eve@example.com", phone="6666666666")

    payload = UserMeUpdateRequest()  # both fields None
    resp = RegisteredUserService.update_me(db_session, user, payload)

    # no change
    assert resp.name == "Eve"
    assert resp.phone == "6666666666"

    fetched = db_session.query(User).get(user.id)
    assert fetched.name == "Eve"
    assert fetched.phone == "6666666666"


def test_update_me_allows_empty_strings(db_session):
    # Since schema doesn't enforce non-empty strings, ensure service writes them as-is
    user = _mk_user(db_session, name="Frank", email="frank@example.com", phone="7777777777")

    payload = UserMeUpdateRequest(name="", phone="")
    resp = RegisteredUserService.update_me(db_session, user, payload)

    assert resp.name == ""
    assert resp.phone == ""

    fetched = db_session.query(User).get(user.id)
    assert fetched.name == ""
    assert fetched.phone == ""
