import pytest
from fastapi.testclient import TestClient
from typing import Callable

from server.models.model import User, UserType, Property, Application, ApplicationStatus
from server.core.security import get_password_hash
from server.api import dependencies as api_deps


@pytest.fixture(autouse=True)
def _cleanup(db_session):
    # Ensure FK-safe cleanup after each test
    yield
    db_session.query(Application).delete()
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


def _mk_property(db, owner: User, name="Nice Home", address="12/3 Street 45", city="Bengaluru", state="KA",
                 pincode="560001", price=1000.0, bedrooms=2, bathrooms=1, area_sqft=800, description="desc") -> Property:
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


def test_create_property_owner_success(client: TestClient, db_session):
    app = client.app
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    _override_current_user(app, owner)

    payload = {
        "name": "Cozy House",
        "address": "123 Cottage Rd",
        "city": "Springfield",
        "state": "IL",
        "pincode": "62704",
        "price": 1500.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "area_sqft": 1200,
        "description": "Great neighborhood",
    }

    r = client.post("/properties/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    # Response model is PropertyResponse: contains id, owner_id, status, timestamps
    assert "id" in data and data["owner_id"] == owner.id
    # Verify persisted fields via DB
    created = db_session.query(Property).get(data["id"])  # SQLAlchemy 1.x style acceptable in tests
    assert created.name == payload["name"]
    assert created.city == payload["city"]
    assert created.price == payload["price"]
    _clear_override(app)


def test_create_property_forbidden_for_tenant(client: TestClient, db_session):
    app = client.app
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)
    _override_current_user(app, tenant)

    payload = {
        "name": "House",
        "address": "1 Main St",
        "city": "City",
        "state": "ST",
        "pincode": "00000",
        "price": 100.0,
        "bedrooms": 1,
        "bathrooms": 1,
        "area_sqft": 400,
        "description": "",
    }

    r = client.post("/properties/", json=payload)
    assert r.status_code == 403
    assert r.json()["detail"] == "Only owners can list a new property"
    _clear_override(app)


def test_search_properties_masks_address_and_filters(client: TestClient, db_session):
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    _mk_property(db_session, owner, name="A", address="12 Alpha Ave", city="York", price=900, bedrooms=2, area_sqft=700)
    _mk_property(db_session, owner, name="B", address="99 Beta St", city="New York", price=2000, bedrooms=4, area_sqft=1200)

    r = client.get("/properties/", params={"city": "York", "max_price": 1500, "min_bedrooms": 2, "min_area": 600})
    assert r.status_code == 200
    data = r.json()
    # Should include both entries matching city contains 'York' and price <= 1500 filters -> only first
    assert len(data) == 1
    item = data[0]
    assert item["city"].lower().find("york") != -1
    # Address digits are masked with 'x'
    assert all(not c.isdigit() for c in item["address"]) and "x" in item["address"]


def test_get_my_properties_only_owner_listed(client: TestClient, db_session):
    app = client.app
    owner1 = _mk_user(db_session, "o1@example.com", UserType.OWNER)
    owner2 = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    _mk_property(db_session, owner1, name="P1")
    _mk_property(db_session, owner2, name="P2")

    _override_current_user(app, owner1)
    r = client.get("/properties/mine")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1 and data[0]["name"] == "P1"
    _clear_override(app)


def test_get_my_property_details_access_control_and_404(client: TestClient, db_session):
    app = client.app
    owner1 = _mk_user(db_session, "o1@example.com", UserType.OWNER)
    owner2 = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner1, address="45 Elm St")

    # Owner can view unmasked address
    _override_current_user(app, owner1)
    r_ok = client.get(f"/properties/{prop.id}/mine")
    assert r_ok.status_code == 200
    assert r_ok.json()["address"] == "45 Elm St"

    # Other owner forbidden
    _override_current_user(app, owner2)
    r_forbidden = client.get(f"/properties/{prop.id}/mine")
    assert r_forbidden.status_code == 403

    # Not found
    r_404 = client.get("/properties/99999/mine")
    assert r_404.status_code == 404
    _clear_override(app)


def test_get_property_details_public_masks_address(client: TestClient, db_session):
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner, address="12 Secret Blvd")

    r = client.get(f"/properties/{prop.id}")
    assert r.status_code == 200
    assert "x" in r.json()["address"] and "Secret" in r.json()["address"]


def test_update_property_owner_success_and_errors(client: TestClient, db_session):
    app = client.app
    owner1 = _mk_user(db_session, "o1@example.com", UserType.OWNER)
    owner2 = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    prop = _mk_property(db_session, owner1, price=1000)

    # Success update by owner1
    _override_current_user(app, owner1)
    r_ok = client.put(f"/properties/{prop.id}", json={"price": 1200})
    assert r_ok.status_code == 200
    # Response model is PropertyResponse; verify persisted change via DB
    updated = db_session.query(Property).get(prop.id)
    assert updated.price == 1200

    # No fields -> 400
    r_bad = client.put(f"/properties/{prop.id}", json={})
    assert r_bad.status_code == 400

    # Different owner -> 403
    _override_current_user(app, owner2)
    r_forbidden = client.put(f"/properties/{prop.id}", json={"price": 1300})
    assert r_forbidden.status_code == 403

    # Not found -> 404
    r_404 = client.put("/properties/99999", json={"price": 100})
    assert r_404.status_code == 404
    _clear_override(app)


def test_manage_application_status_success_and_errors(client: TestClient, db_session):
    app = client.app
    owner1 = _mk_user(db_session, "o1@example.com", UserType.OWNER)
    owner2 = _mk_user(db_session, "o2@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "t@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner1)

    # Create an application directly
    app_obj = Application(property_id=prop.id, tenant_id=tenant.id)
    db_session.add(app_obj)
    db_session.commit()
    db_session.refresh(app_obj)

    # Owner1 can accept
    _override_current_user(app, owner1)
    r_ok = client.put(f"/applications/{app_obj.id}", json={"status": "accepted"})
    assert r_ok.status_code == 200
    assert r_ok.json()["status"] == ApplicationStatus.ACCEPTED.value

    # Other owner forbidden
    _override_current_user(app, owner2)
    r_forbidden = client.put(f"/applications/{app_obj.id}", json={"status": "rejected"})
    assert r_forbidden.status_code == 403

    # Application not found
    r_404 = client.put("/applications/99999", json={"status": "viewed"})
    assert r_404.status_code == 404

    # Simulate missing property for the application
    app_obj.property_id = 99999
    db_session.add(app_obj)
    db_session.commit()

    _override_current_user(app, owner1)
    r_missing_prop = client.put(f"/applications/{app_obj.id}", json={"status": "viewed"})
    assert r_missing_prop.status_code == 404
    _clear_override(app)


def test_apply_and_list_applications_tenant_and_owner_rules(client: TestClient, db_session):
    app = client.app
    owner = _mk_user(db_session, "owner@example.com", UserType.OWNER)
    tenant = _mk_user(db_session, "tenant@example.com", UserType.TENANT)
    prop = _mk_property(db_session, owner)

    # Tenant can apply
    _override_current_user(app, tenant)
    r_apply = client.post("/applications/", json={"property_id": prop.id})
    assert r_apply.status_code == 201

    # Tenant sees own applications
    r_list = client.get("/applications/")
    assert r_list.status_code == 200
    apps = r_list.json()
    assert len(apps) == 1 and apps[0]["tenant_id"] == tenant.id

    # Owner cannot apply
    _override_current_user(app, owner)
    r_forbidden = client.post("/applications/", json={"property_id": prop.id})
    assert r_forbidden.status_code == 403

    # 404 missing property
    _override_current_user(app, tenant)
    r_404 = client.post("/applications/", json={"property_id": 99999})
    assert r_404.status_code == 404

    _clear_override(app)
