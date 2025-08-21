import pytest
from sqlalchemy.exc import IntegrityError, StatementError

from server.models.model import (
    User, UserType,
    Property, PropertyStatus,
    Application, ApplicationStatus,
    ShortlistedProperty,
)


@pytest.fixture(autouse=True)
def _cleanup_db(db_session):
    """Ensure tables are cleaned between tests (since we commit in tests).
    Delete in FK-safe order.
    """
    try:
        yield
    finally:
        # Ensure session is usable even if the test failed during commit/flush
        try:
            db_session.rollback()
        except Exception:
            pass
        # Teardown: delete children first
        db_session.query(ShortlistedProperty).delete()
        db_session.query(Application).delete()
        db_session.query(Property).delete()
        db_session.query(User).delete()
        db_session.commit()


def _create_user(db_session, email="owner@example.com", user_type=UserType.OWNER):
    u = User(
        name="Owner",
        email=email,
        phone="9999999999",
        password_hash="hashed",
        user_type=user_type,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


def _create_property(db_session, owner, **overrides):
    p = Property(
        owner_id=owner.id,
        name=overrides.get("name", "Apt"),
        address=overrides.get("address", "123 Street"),
        city=overrides.get("city", "City"),
        state=overrides.get("state", "State"),
        pincode=overrides.get("pincode", "560001"),
        price=overrides.get("price", 1500.0),
        bedrooms=overrides.get("bedrooms", 2),
        bathrooms=overrides.get("bathrooms", 1),
        area_sqft=overrides.get("area_sqft", 700),
        description=overrides.get("description", None),
        status=overrides.get("status", PropertyStatus.AVAILABLE),
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


# ------------------- Constraints and Uniqueness -------------------

def test_user_unique_email_constraint(db_session):
    _create_user(db_session, email="unique@example.com")
    with pytest.raises(IntegrityError):
        _create_user(db_session, email="unique@example.com")


# ------------------- Relationships -------------------

def test_property_belongs_to_owner_and_backref(db_session):
    owner = _create_user(db_session)
    prop = _create_property(db_session, owner)

    # Forward relation
    assert prop.owner_id == owner.id
    assert prop.owner.email == owner.email

    # Back-populates
    assert len(owner.properties) == 1
    assert owner.properties[0].id == prop.id


def test_application_relationships_and_status_default(db_session):
    owner = _create_user(db_session, email="own2@example.com", user_type=UserType.OWNER)
    tenant = _create_user(db_session, email="ten1@example.com", user_type=UserType.TENANT)
    prop = _create_property(db_session, owner)

    app = Application(property_id=prop.id, tenant_id=tenant.id)
    db_session.add(app)
    db_session.commit()
    db_session.refresh(app)

    # Defaults and relations
    assert app.status == ApplicationStatus.SENT
    assert app.property.id == prop.id
    assert app.tenant.id == tenant.id


def test_shortlisted_property_relationships(db_session):
    owner = _create_user(db_session, email="own3@example.com", user_type=UserType.OWNER)
    tenant = _create_user(db_session, email="ten2@example.com", user_type=UserType.TENANT)
    prop = _create_property(db_session, owner)

    s = ShortlistedProperty(user_id=tenant.id, property_id=prop.id)
    db_session.add(s)
    db_session.commit()
    db_session.refresh(s)

    assert s.user.id == tenant.id
    assert s.property.id == prop.id


# ------------------- Enums and Defaults -------------------

def test_property_status_default_is_available(db_session):
    owner = _create_user(db_session, email="own4@example.com")
    p = _create_property(db_session, owner)
    assert p.status == PropertyStatus.AVAILABLE


def test_invalid_enum_value_rejected(db_session):
    owner = _create_user(db_session, email="own5@example.com")
    p = _create_property(db_session, owner)

    # Constructing PropertyStatus with an invalid value must raise ValueError
    with pytest.raises(ValueError):
        # This raises at Enum construction time, independent of DB constraints
        p.status = PropertyStatus("not_a_valid_status")  # type: ignore[arg-type]
    db_session.rollback()


# ------------------- Not-null constraints (sample) -------------------

def test_property_requires_owner_id(db_session):
    p = Property(
        owner_id=None,  # type: ignore
        name="No Owner",
        address="123",
        city="C",
        state="S",
        pincode="560001",
        price=1000.0,
        bedrooms=1,
        bathrooms=1,
        area_sqft=400,
        description=None,
        status=PropertyStatus.AVAILABLE,
    )
    db_session.add(p)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
