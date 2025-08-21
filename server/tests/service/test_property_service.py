import pytest
from fastapi import HTTPException

from server.services.property_service import PropertyService
from server.models.model import User, UserType, Property, Application, ApplicationStatus
from server.schemas.schema import PropertyCreate, PropertyUpdate, ApplicationUpdateRequest


# -------------------- fixtures & helpers --------------------

@pytest.fixture(autouse=True)
def _cleanup_tables(db_session):
    """Ensure isolation: clean dependent tables after each test."""
    try:
        yield
    finally:
        try:
            db_session.rollback()
        except Exception:
            pass
        db_session.query(Application).delete()
        db_session.query(Property).delete()
        db_session.query(User).delete()
        db_session.commit()


def _mk_user(db_session, email: str, user_type: UserType) -> User:
    u = User(
        name="U",
        email=email,
        phone="0000000000",
        password_hash="h",
        user_type=user_type,
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


def _mk_property(db_session, owner: User, **overrides) -> Property:
    payload = PropertyCreate(
        name=overrides.get("name", "Home"),
        address=overrides.get("address", "123 St"),
        city=overrides.get("city", "City"),
        state=overrides.get("state", "State"),
        pincode=overrides.get("pincode", "560001"),
        price=overrides.get("price", 1500.0),
        bedrooms=overrides.get("bedrooms", 2),
        bathrooms=overrides.get("bathrooms", 1),
        area_sqft=overrides.get("area_sqft", 700),
        description=overrides.get("description", None),
    )
    return PropertyService.create_property(db_session, payload, owner_id=owner.id)


# -------------------- create_property --------------------

def test_create_property_allows_only_owners(db_session):
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    payload = PropertyCreate(
        name="A", address="a", city="c", state="s", pincode="560001",
        price=1000.0, bedrooms=1, bathrooms=1, area_sqft=400, description=None,
    )
    with pytest.raises(HTTPException) as ei:
        PropertyService.create_property(db_session, payload, owner_id=tenant.id)
    assert ei.value.status_code == 403


def test_create_property_success_for_owner(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner, name="Nice Apt", city="Bangalore", price=2500.0)
    assert prop.id > 0
    assert prop.owner_id == owner.id
    assert prop.name == "Nice Apt"
    assert prop.city == "Bangalore"
    # persisted
    in_db = db_session.query(Property).filter(Property.id == prop.id).first()
    assert in_db is not None


# -------------------- listing & search --------------------

def test_get_all_and_by_owner_and_pagination(db_session):
    owner1 = _mk_user(db_session, "o1@example.com", UserType.OWNER)
    owner2 = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    p1 = _mk_property(db_session, owner1, name="P1")
    p2 = _mk_property(db_session, owner1, name="P2")
    p3 = _mk_property(db_session, owner2, name="P3")

    # get_all with skip/limit
    all_props = PropertyService.get_all_properties(db_session, skip=1, limit=2)
    assert len(all_props) <= 2

    # by owner
    o1_props = PropertyService.get_properties_by_owner(db_session, owner1.id)
    ids = sorted([p.id for p in o1_props])
    assert set(ids) == {p1.id, p2.id}


def test_search_properties_filters(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    _mk_property(db_session, owner, name="C1", city="Bangalore", price=1500.0, bedrooms=2, area_sqft=600)
    _mk_property(db_session, owner, name="C2", city="Mumbai", price=3000.0, bedrooms=3, area_sqft=900)
    _mk_property(db_session, owner, name="C3", city="Bengal", price=1200.0, bedrooms=1, area_sqft=450)

    # city ilike
    res = PropertyService.search_properties(db_session, city="banga")
    assert all("banga" in p.city.lower() for p in res)

    # max_price
    res = PropertyService.search_properties(db_session, max_price=1500.0)
    assert all(p.price <= 1500.0 for p in res)

    # min_bedrooms
    res = PropertyService.search_properties(db_session, min_bedrooms=2)
    assert all(p.bedrooms >= 2 for p in res)

    # min_area
    res = PropertyService.search_properties(db_session, min_area=600)
    assert all(p.area_sqft >= 600 for p in res)


# -------------------- get_property_by_id --------------------

def test_get_property_by_id_success_and_404(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner)

    found = PropertyService.get_property_by_id(db_session, prop.id)
    assert found.id == prop.id

    with pytest.raises(HTTPException) as ei:
        PropertyService.get_property_by_id(db_session, 999999)
    assert ei.value.status_code == 404


# -------------------- update_property --------------------

def test_update_property_not_found_and_forbidden_and_empty(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    other = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner, name="Old", city="X")

    # not found
    with pytest.raises(HTTPException) as ei:
        PropertyService.update_property(db_session, 99999, owner.id, PropertyUpdate())
    assert ei.value.status_code == 404

    # forbidden (different owner)
    with pytest.raises(HTTPException) as ei:
        PropertyService.update_property(db_session, prop.id, other.id, PropertyUpdate(name="New"))
    assert ei.value.status_code == 403

    # empty update payload -> 400
    with pytest.raises(HTTPException) as ei:
        PropertyService.update_property(db_session, prop.id, owner.id, PropertyUpdate())
    assert ei.value.status_code == 400


def test_update_property_success_partial_fields(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner, name="Old Name", city="Old City", price=1000.0)

    updates = PropertyUpdate(name="New Name", price=2000.0)
    updated = PropertyService.update_property(db_session, prop.id, owner.id, updates)

    assert updated.name == "New Name"
    assert updated.price == 2000.0
    assert updated.city == "Old City"  # unchanged


# -------------------- manage_application --------------------

def test_manage_application_paths(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    other = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner)

    # not found application
    with pytest.raises(HTTPException) as ei:
        PropertyService.manage_application(
            db_session, application_id=99999, owner_id=owner.id, payload=ApplicationUpdateRequest(status="viewed")
        )
    assert ei.value.status_code == 404

    # create an application
    app = Application(property_id=prop.id, tenant_id=tenant.id, status=ApplicationStatus.SENT)
    db_session.add(app)
    db_session.commit()
    db_session.refresh(app)

    # property not found for application (simulate by pointing to a non-existent property id)
    app.property_id = 999999  # ensure this ID does not exist
    db_session.add(app)
    db_session.commit()
    with pytest.raises(HTTPException) as ei:
        PropertyService.manage_application(
            db_session, application_id=app.id, owner_id=owner.id, payload=ApplicationUpdateRequest(status="viewed")
        )
    assert ei.value.status_code == 404

    # recreate property and link again
    prop2 = _mk_property(db_session, owner)
    app.property_id = prop2.id
    db_session.add(app)
    db_session.commit()

    # forbidden owner
    with pytest.raises(HTTPException) as ei:
        PropertyService.manage_application(
            db_session, application_id=app.id, owner_id=other.id, payload=ApplicationUpdateRequest(status="viewed")
        )
    assert ei.value.status_code == 403

    # allowed transitions
    for target in ("viewed", "accepted", "rejected"):
        updated = PropertyService.manage_application(
            db_session, application_id=app.id, owner_id=owner.id, payload=ApplicationUpdateRequest(status=target)
        )
        assert updated.status.name.lower() == target


# -------------------- delete_property --------------------

def test_delete_property_paths_and_cascade_cleanup(db_session):
    owner = _mk_user(db_session, "o@example.com", UserType.OWNER)
    other = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner)

    # Not found
    with pytest.raises(HTTPException) as ei:
        PropertyService.delete_property(db_session, 99999, owner.id)
    assert ei.value.status_code == 404

    # Forbidden
    with pytest.raises(HTTPException) as ei:
        PropertyService.delete_property(db_session, prop.id, other.id)
    assert ei.value.status_code == 403

    # Create applications and ensure they are removed when property is deleted
    a1 = Application(property_id=prop.id, tenant_id=tenant.id, status=ApplicationStatus.SENT)
    a2 = Application(property_id=prop.id, tenant_id=tenant.id, status=ApplicationStatus.SENT)
    db_session.add_all([a1, a2])
    db_session.commit()

    deleted_id = PropertyService.delete_property(db_session, prop.id, owner.id)
    assert deleted_id == prop.id

    # applications for that property should be gone
    remaining_apps = db_session.query(Application).filter(Application.property_id == prop.id).all()
    assert remaining_apps == []
