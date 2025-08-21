"""
Pytest test configuration for the server package.
Fixtures for DB/app/auth overrides will be added next.
"""

import os
import sys
from pathlib import Path
import pytest
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# IMPORTANT: configure test DB URL BEFORE importing the app/db modules
# Use a file-based SQLite DB to allow multiple connections/threads in tests
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_db.sqlite3")

# Ensure the main app picks this up when it constructs its engine on import
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)

# Ensure repo root is on sys.path so 'import server.*' works when running from server/
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from server.db.database import Base  # noqa: E402
from server.models import model as models  # noqa: F401,E402  ensure models are imported so tables are registered

# Create a dedicated test engine (separate from app's SessionLocal)
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables once for the test database (models imported above register tables)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    db = TestingSessionLocal()
    try:
        yield db
        db.rollback()
    finally:
        db.close()


@pytest.fixture(scope="session")
def app():
    """Import and return the FastAPI app."""
    # Inject a dummy path_setup module to satisfy server.main import without editing app code
    import types
    import sys as _sys
    if "path_setup" not in _sys.modules:
        _sys.modules["path_setup"] = types.ModuleType("path_setup")

    from server.main import app as fastapi_app  # import after env is set
    return fastapi_app


@pytest.fixture(scope="function")
def override_dependencies(app, db_session):
    """Override FastAPI dependencies (get_db, get_current_user) for tests."""
    from server.db.database import get_db
    from server.models.model import User, UserType
    from server.api import dependencies as api_deps

    # Override get_db to use the test session
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override

    # Provide a stubbed authenticated user for protected endpoints
    def _current_user_override():
        # Persist once per test so that ID is available when needed
        user = db_session.query(User).filter(User.email == "test@example.com").first()
        if not user:
            user = User(
                name="Test User",
                email="test@example.com",
                phone="0000000000",
                password_hash="hashed",
                user_type=UserType.OWNER,
            )
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
        return user

    app.dependency_overrides[api_deps.get_current_user] = _current_user_override

    yield

    # Cleanup overrides after each test
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(app, override_dependencies):
    from fastapi.testclient import TestClient
    return TestClient(app)
