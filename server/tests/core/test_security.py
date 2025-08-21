import time
from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from server.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
)
from server.core import config as core_config


@pytest.fixture
def credentials_exception():
    class CredExc(Exception):
        pass
    return CredExc


# Password hashing tests

def test_password_hash_and_verify_success_and_failure():
    password = "S3cret!"
    wrong = "not-it"

    h1 = get_password_hash(password)
    h2 = get_password_hash(password)

    # Hashes should be non-empty and different (salted)
    assert isinstance(h1, str) and isinstance(h2, str)
    assert h1 != h2

    # Correct verification
    assert verify_password(password, h1) is True
    assert verify_password(password, h2) is True

    # Incorrect password
    assert verify_password(wrong, h1) is False
    assert verify_password(wrong, h2) is False


# JWT create and verify tests

def test_create_access_token_with_custom_exp_and_verify(credentials_exception):
    settings = core_config.settings
    subject = "user@example.com"

    # Short expiry 2 seconds
    token = create_access_token({"sub": subject}, expires_delta=timedelta(seconds=2))
    assert isinstance(token, str) and token

    # Decode and inspect claims
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded.get("sub") == subject
    assert "exp" in decoded

    # Verify helper returns subject
    result = verify_token(token, credentials_exception)
    assert result == subject


def test_verify_token_raises_when_missing_sub(credentials_exception):
    settings = core_config.settings
    # Manually create a token without sub
    payload = {"foo": "bar"}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    with pytest.raises(credentials_exception):
        verify_token(token, credentials_exception)


def test_verify_token_raises_on_expired(credentials_exception):
    settings = core_config.settings
    # Create an already expired token
    token = create_access_token({"sub": "x@y.z"}, expires_delta=timedelta(seconds=-1))

    with pytest.raises(credentials_exception):
        verify_token(token, credentials_exception)


def test_verify_token_raises_on_invalid_signature(credentials_exception):
    settings = core_config.settings
    subject = "user@example.com"

    # Token signed with wrong secret
    wrong_secret = settings.SECRET_KEY + "-tampered"
    token = jwt.encode({"sub": subject}, wrong_secret, algorithm=settings.ALGORITHM)

    with pytest.raises(credentials_exception):
        verify_token(token, credentials_exception)


def test_create_access_token_default_expiry_is_future():
    settings = core_config.settings
    now = datetime.now(timezone.utc)
    token = create_access_token({"sub": "a@b.c"})

    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    # Default expiry should be in the future and roughly ACCESS_TOKEN_EXPIRE_MINUTES
    assert exp > now
    approx = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # Allow drift of +/- 60 seconds
    assert abs((exp - approx).total_seconds()) < 60
