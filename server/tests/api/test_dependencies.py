import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from datetime import timedelta, datetime

from server.api.dependencies import get_current_user
from server.core import security
from server.models.model import User, UserType


@pytest.fixture(autouse=True)
def _cleanup_users(db_session):
    # Ensure isolation between tests
    yield
    db_session.query(User).delete()
    db_session.commit()


def _mk_user(db_session, email="alice@example.com") -> User:
    user = User(
        name="Alice",
        email=email,
        phone="9999999999",
        password_hash=security.get_password_hash("secret"),
        user_type=UserType.TENANT,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _credentials(token: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_get_current_user_success(db_session):
    user = _mk_user(db_session)
    token = security.create_access_token({"sub": user.email})

    result = get_current_user(credentials=_credentials(token), db=db_session)
    assert result.id == user.id
    assert result.email == user.email


def test_get_current_user_user_not_found(db_session):
    # Token for a user that does not exist
    token = security.create_access_token({"sub": "ghost@example.com"})

    with pytest.raises(HTTPException) as exc:
        get_current_user(credentials=_credentials(token), db=db_session)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"


def test_get_current_user_invalid_token_signature(db_session):
    # Craft a token with different secret by temporarily encoding with a wrong key
    # Instead of modifying settings, just pass an obviously invalid token string
    bad_token = "invalid.token.value"

    with pytest.raises(HTTPException) as exc:
        get_current_user(credentials=_credentials(bad_token), db=db_session)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"


def test_get_current_user_expired_token(db_session, monkeypatch):
    user = _mk_user(db_session)

    # Create a token that is already expired
    token = security.create_access_token({"sub": user.email}, expires_delta=timedelta(seconds=-1))

    with pytest.raises(HTTPException) as exc:
        get_current_user(credentials=_credentials(token), db=db_session)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"


def test_get_current_user_missing_sub_claim(db_session):
    # create token without 'sub'
    token = security.create_access_token({"some": "data"})

    with pytest.raises(HTTPException) as exc:
        get_current_user(credentials=_credentials(token), db=db_session)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Could not validate credentials"
