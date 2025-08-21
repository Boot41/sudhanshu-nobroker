import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from server.services.tenant_service import TenantService
from server.models.model import (
    User,
    UserType,
    Property,
    ShortlistedProperty,
    Application,
)
from server.schemas.schema import ShortlistRequest


# -------------------- fixtures & helpers --------------------

@pytest.fixture(autouse=True)
def _cleanup_tables(db_session):
    """Ensure isolation: clean dependent tables after each test in FK-safe order."""
    try:
        yield
    finally:
        try:
            db_session.rollback()
        except Exception:
            pass
        # FK-safe deletion order
        db_session.query(Application).delete()
        db_session.query(ShortlistedProperty).delete()
        db_session.query(Property).delete()
        db_session.query(User).delete()
        db_session.commit()


def _mk_user(db_session, email: str, user_type: UserType, name: str = "User", phone: str = "0000000000") -> User:
    u = User(name=name, email=email, phone=phone, password_hash="hash", user_type=user_type)
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


def _mk_property(
    db_session,
    owner: User,
    name: str = "P1",
    address: str = "Addr",
    city: str = "City",
    state: str = "State",
    pincode: str = "000000",
    price: float = 1000.0,
    bedrooms: int = 1,
    bathrooms: int = 1,
    area_sqft: int = 500,
    description: str | None = None,
) -> Property:
    p = Property(
        owner_id=owner.id,
        name=name,
        address=address,
        city=city,
        state=state,
        pincode=pincode,
        price=price,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        area_sqft=area_sqft,
        description=description,
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


# -------------------- tests: shortlist_property --------------------

def test_shortlist_property_forbidden_non_tenant(db_session):
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    other_owner = _mk_user(db_session, "owner2@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner=other_owner)

    with pytest.raises(HTTPException) as ei:
        TenantService.shortlist_property(db_session, tenant_id=owner.id, payload=ShortlistRequest(property_id=prop.id))
    assert ei.value.status_code == 403


def test_shortlist_property_property_not_found(db_session):
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)

    with pytest.raises(HTTPException) as ei:
        TenantService.shortlist_property(db_session, tenant_id=tenant.id, payload=ShortlistRequest(property_id=999999))
    assert ei.value.status_code == 404


def test_shortlist_property_success_and_idempotent(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner=owner)

    entry1 = TenantService.shortlist_property(db_session, tenant_id=tenant.id, payload=ShortlistRequest(property_id=prop.id))
    entry2 = TenantService.shortlist_property(db_session, tenant_id=tenant.id, payload=ShortlistRequest(property_id=prop.id))

    assert entry1.id == entry2.id  # idempotent

    cnt = (
        db_session.query(ShortlistedProperty)
        .filter(ShortlistedProperty.user_id == tenant.id, ShortlistedProperty.property_id == prop.id)
        .count()
    )
    assert cnt == 1


# -------------------- tests: get_shortlisted_properties --------------------

def test_get_shortlisted_properties_forbidden_non_tenant(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    with pytest.raises(HTTPException) as ei:
        TenantService.get_shortlisted_properties(db_session, tenant_id=owner.id)
    assert ei.value.status_code == 403


def test_get_shortlisted_properties_lists_properties(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    p1 = _mk_property(db_session, owner=owner, name="P1")
    p2 = _mk_property(db_session, owner=owner, name="P2")

    TenantService.shortlist_property(db_session, tenant_id=tenant.id, payload=ShortlistRequest(property_id=p1.id))
    TenantService.shortlist_property(db_session, tenant_id=tenant.id, payload=ShortlistRequest(property_id=p2.id))

    props = TenantService.get_shortlisted_properties(db_session, tenant_id=tenant.id)
    ids = {prop.id for prop in props}
    assert ids == {p1.id, p2.id}


# -------------------- tests: remove_shortlisted_property --------------------

def test_remove_shortlisted_property_forbidden_non_tenant(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    with pytest.raises(HTTPException) as ei:
        TenantService.remove_shortlisted_property(db_session, tenant_id=owner.id, property_id=1)
    assert ei.value.status_code == 403


def test_remove_shortlisted_property_not_found(db_session):
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    with pytest.raises(HTTPException) as ei:
        TenantService.remove_shortlisted_property(db_session, tenant_id=tenant.id, property_id=12345)
    assert ei.value.status_code == 404


def test_remove_shortlisted_property_success(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner=owner)

    TenantService.shortlist_property(db_session, tenant_id=tenant.id, payload=ShortlistRequest(property_id=prop.id))

    TenantService.remove_shortlisted_property(db_session, tenant_id=tenant.id, property_id=prop.id)

    # ensure deletion
    cnt = (
        db_session.query(ShortlistedProperty)
        .filter(ShortlistedProperty.user_id == tenant.id, ShortlistedProperty.property_id == prop.id)
        .count()
    )
    assert cnt == 0


# -------------------- tests: apply_for_property --------------------

def test_apply_for_property_forbidden_non_tenant(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    with pytest.raises(HTTPException) as ei:
        TenantService.apply_for_property(db_session, tenant_id=owner.id, property_id=1)
    assert ei.value.status_code == 403


def test_apply_for_property_property_not_found(db_session):
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    with pytest.raises(HTTPException) as ei:
        TenantService.apply_for_property(db_session, tenant_id=tenant.id, property_id=999999)
    assert ei.value.status_code == 404


def test_apply_for_property_own_property_bad_request(db_session):
    # Use a TENANT who also owns the property (owner_id points to this tenant)
    tenant_owner = _mk_user(db_session, "to@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner=tenant_owner)

    with pytest.raises(HTTPException) as ei:
        TenantService.apply_for_property(db_session, tenant_id=tenant_owner.id, property_id=prop.id)
    assert ei.value.status_code == 400


def test_apply_for_property_success_and_idempotent(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner=owner)

    a1 = TenantService.apply_for_property(db_session, tenant_id=tenant.id, property_id=prop.id)
    a2 = TenantService.apply_for_property(db_session, tenant_id=tenant.id, property_id=prop.id)

    assert a1.id == a2.id

    cnt = (
        db_session.query(Application)
        .filter(Application.property_id == prop.id, Application.tenant_id == tenant.id)
        .count()
    )
    assert cnt == 1


# -------------------- tests: get_my_applications --------------------

def test_get_my_applications_forbidden_non_tenant(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    with pytest.raises(HTTPException) as ei:
        TenantService.get_my_applications(db_session, tenant_id=owner.id)
    assert ei.value.status_code == 403


def test_get_my_applications_orders_desc_by_created_at(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    p1 = _mk_property(db_session, owner=owner, name="P1")
    p2 = _mk_property(db_session, owner=owner, name="P2")

    a1 = TenantService.apply_for_property(db_session, tenant_id=tenant.id, property_id=p1.id)
    a2 = TenantService.apply_for_property(db_session, tenant_id=tenant.id, property_id=p2.id)

    # Ensure deterministic ordering: a2 newer than a1
    earlier = datetime.utcnow() - timedelta(seconds=10)
    later = datetime.utcnow()
    a1.created_at = earlier
    a2.created_at = later
    db_session.add_all([a1, a2])
    db_session.commit()

    apps = TenantService.get_my_applications(db_session, tenant_id=tenant.id)
    assert [a.id for a in apps] == [a2.id, a1.id]
