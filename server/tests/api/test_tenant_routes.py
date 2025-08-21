import pytest
from fastapi.testclient import TestClient

from server.models.model import User, UserType, Property, ShortlistedProperty
from server.core.security import get_password_hash
from server.api import dependencies as api_deps


@pytest.fixture(autouse=True)
def _cleanup(db_session):
    # FK-safe cleanup
    yield
    db_session.query(ShortlistedProperty).delete()
    db_session.query(Property).delete()
    db_session.query(User).delete()
    db_session.commit()


def _mk_user(db, email: str, user_type: UserType) -> User:
    u = User(
        name=email.split("@")[0],
        email=email,
        phone="1234567890",
        password_hash=get_password_hash("pass"),
        user_type=user_type,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _mk_property(db, owner: User, name="Unit", address="12/3 Rd", city="City", state="ST",
                 pincode="00000", price=1000.0, bedrooms=2, bathrooms=1, area_sqft=700, description="") -> Property:
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
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def _override_current_user(app, user: User):
    app.dependency_overrides[api_deps.get_current_user] = lambda: user


def _clear_override(app):
    app.dependency_overrides.pop(api_deps.get_current_user, None)


def test_shortlist_property_success_and_idempotent(client: TestClient, db_session):
    app = client.app
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner)

    _override_current_user(app, tenant)
    r1 = client.post("/me/shortlist", json={"property_id": prop.id})
    assert r1.status_code == 200
    body1 = r1.json()
    assert body1["user_id"] == tenant.id and body1["property_id"] == prop.id

    # idempotent: same call returns same shortlist entry
    r2 = client.post("/me/shortlist", json={"property_id": prop.id})
    assert r2.status_code == 200
    body2 = r2.json()
    assert body2["id"] == body1["id"]
    _clear_override(app)


def test_shortlist_property_forbidden_for_owner_and_404_missing_property(client: TestClient, db_session):
    app = client.app
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    _override_current_user(app, owner)

    # forbidden for owner
    r_forbidden = client.post("/me/shortlist", json={"property_id": 1})
    assert r_forbidden.status_code == 403

    # as tenant but property missing -> 404
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)
    _override_current_user(app, tenant)
    r_404 = client.post("/me/shortlist", json={"property_id": 99999})
    assert r_404.status_code == 404
    _clear_override(app)


def test_get_shortlist_lists_properties_and_forbidden_for_owner(client: TestClient, db_session):
    app = client.app
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)
    p1 = _mk_property(db_session, owner, name="P1")
    p2 = _mk_property(db_session, owner, name="P2")

    # Pre-populate shortlist
    db_session.add(ShortlistedProperty(user_id=tenant.id, property_id=p1.id))
    db_session.add(ShortlistedProperty(user_id=tenant.id, property_id=p2.id))
    db_session.commit()

    _override_current_user(app, tenant)
    r = client.get("/me/shortlist")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    # Response model is PropertyResponse; verify by IDs instead of name
    ids = {item["id"] for item in data}
    assert ids == {p1.id, p2.id}

    # Owner cannot list shortlist
    _override_current_user(app, owner)
    r_forbidden = client.get("/me/shortlist")
    assert r_forbidden.status_code == 403
    _clear_override(app)


def test_remove_from_shortlist_success_and_errors(client: TestClient, db_session):
    app = client.app
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)
    p = _mk_property(db_session, owner)

    # Add one entry
    entry = ShortlistedProperty(user_id=tenant.id, property_id=p.id)
    db_session.add(entry)
    db_session.commit()

    # Tenant can remove -> 204
    _override_current_user(app, tenant)
    r_del = client.delete(f"/me/shortlist/{p.id}")
    assert r_del.status_code == 204

    # Removing again -> 404
    r_404 = client.delete(f"/me/shortlist/{p.id}")
    assert r_404.status_code == 404

    # Owner cannot remove -> 403
    _override_current_user(app, owner)
    r_forbidden = client.delete(f"/me/shortlist/{p.id}")
    assert r_forbidden.status_code == 403
    _clear_override(app)
