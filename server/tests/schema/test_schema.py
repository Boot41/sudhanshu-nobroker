import pytest
from types import SimpleNamespace
from datetime import datetime

from schemas.schema import (
    UserRegistrationRequest,
    UserResponse,
    UserRegistrationResponse,
    ErrorResponse,
    UserMeResponse,
    UserMeUpdateRequest,
    UserLoginRequest,
    Token,
    PropertyBase,
    PropertyCreate,
    Property,
    PropertyUpdate,
    PropertySearchQuery,
    PropertyDeleteResponse,
    PropertyPublic,
    PropertyOwnerItem,
    PropertyOwnerDetail,
    ApplicationResponse,
    ApplicationUpdateRequest,
    ApplicationCreateRequest,
    ShortlistRequest,
    ShortlistResponse,
)
from server.models.model import PropertyStatus, ApplicationStatus, UserType


# Optional setup/teardown for the module (schemas are pure, so these are no-ops)

def setup_module(module):
    # Placeholder for any per-module setup if needed later
    pass


def teardown_module(module):
    # Placeholder for any per-module teardown if needed later
    pass


# ------------------------- User Schemas -------------------------

def test_user_registration_request_valid():
    m = UserRegistrationRequest(
        name="Alice",
        email="alice@example.com",
        phone="1234567890",
        password="secret",
        user_type="owner",
    )
    assert m.user_type == "owner"


def test_user_registration_request_invalid_email():
    with pytest.raises(Exception):
        UserRegistrationRequest(
            name="Bob",
            email="not-an-email",
            phone="123",
            password="pwd",
            user_type="tenant",
        )


def test_user_registration_request_invalid_user_type():
    with pytest.raises(Exception):
        UserRegistrationRequest(
            name="Charlie",
            email="charlie@example.com",
            phone="123",
            password="pwd",
            user_type="admin",  # not allowed; must be "tenant" or "owner"
        )


def test_user_response_from_attributes():
    now = datetime.utcnow()
    obj = SimpleNamespace(
        id=1,
        name="Dana",
        email="dana@example.com",
        phone="5551112222",
        user_type=UserType.OWNER.value,
        created_at=now,
    )
    m = UserResponse.model_validate(obj)
    assert m.id == 1 and m.created_at == now


def test_user_registration_response_shape():
    now = datetime.utcnow()
    m = UserRegistrationResponse(
        id=10,
        name="Eve",
        email="eve@example.com",
        phone="999",
        user_type="tenant",
        message="Registered",
        created_at=now,
    )
    dumped = m.model_dump()
    assert dumped["message"] == "Registered" and dumped["id"] == 10


def test_user_me_response_email_validation():
    now = datetime.utcnow()
    m = UserMeResponse(
        id=2,
        name="Frank",
        email="frank@example.com",
        phone="123456",
        user_type="owner",
        created_at=now,
    )
    assert m.email == "frank@example.com"
    with pytest.raises(Exception):
        UserMeResponse(
            id=3,
            name="Gina",
            email="bad",
            phone="123",
            user_type="tenant",
            created_at=now,
        )


def test_user_me_update_request_partial():
    m = UserMeUpdateRequest(name="New Name")
    assert m.name == "New Name" and m.phone is None


def test_user_login_and_token():
    login = UserLoginRequest(email="x@example.com", password="pwd")
    assert login.email == "x@example.com"
    token = Token(access_token="abc", token_type="bearer")
    assert token.token_type == "bearer"


def test_error_response_shape():
    e = ErrorResponse(error="BadRequest", detail="Invalid input")
    assert "Invalid" in e.detail


# ------------------------- Property Schemas -------------------------

def _valid_property_base_kwargs():
    return dict(
        name="Nice Flat",
        address="123 Street",
        city="City",
        state="State",
        pincode="560001",
        price=12000.50,
        bedrooms=2,
        bathrooms=2,
        area_sqft=900,
        description="Good ventilation",
    )


def test_property_base_and_create_valid():
    base = PropertyBase(**_valid_property_base_kwargs())
    assert base.bedrooms == 2 and base.description is not None
    created = PropertyCreate(**_valid_property_base_kwargs())
    assert created.city == "City"


def test_property_base_type_errors():
    bad = _valid_property_base_kwargs()
    bad["price"] = "free"
    with pytest.raises(Exception):
        PropertyBase(**bad)


def test_property_update_all_optional_and_partial():
    u = PropertyUpdate()
    assert u.model_dump(exclude_none=True) == {}
    u2 = PropertyUpdate(price=10000.0, description="Updated")
    d = u2.model_dump(exclude_none=True)
    assert d["price"] == 10000.0 and d["description"] == "Updated"


def test_property_search_query_defaults_and_types():
    q = PropertySearchQuery()
    assert q.skip == 0 and q.limit == 100
    q2 = PropertySearchQuery(city="City", max_price=15000.0, min_bedrooms=2, min_area=800)
    assert q2.max_price == 15000.0 and q2.min_area == 800


def test_property_delete_response():
    r = PropertyDeleteResponse(id=5, message="Deleted")
    assert r.id == 5 and r.message == "Deleted"


def test_property_public_shape():
    p = PropertyPublic(
        name="Nice",
        address="Masked",
        city="C",
        state="S",
        pincode="560001",
        price=1000.0,
        bedrooms=1,
        bathrooms=1,
        area_sqft=500,
    )
    assert p.area_sqft == 500


def test_property_owner_item_and_detail_with_enum():
    now = datetime.utcnow()
    item = PropertyOwnerItem(
        id=1,
        name="Apt",
        city="C",
        state="S",
        price=1500.0,
        bedrooms=2,
        bathrooms=1,
        area_sqft=700,
    )
    assert item.id == 1 and item.price == 1500.0

    detail = PropertyOwnerDetail(
        id=2,
        name="Apt",
        address="Full Address",
        city="C",
        state="S",
        pincode="560001",
        price=2000.0,
        bedrooms=3,
        bathrooms=2,
        area_sqft=1000,
        description=None,
        status=PropertyStatus.AVAILABLE,
        owner_id=10,
        created_at=now,
        updated_at=None,
    )
    assert detail.status == PropertyStatus.AVAILABLE and detail.owner_id == 10


def test_property_model_from_attributes_with_nested_owner():
    now = datetime.utcnow()
    owner_obj = SimpleNamespace(
        id=99,
        name="Owner",
        email="owner@example.com",
        phone="111",
        user_type="owner",
        created_at=now,
    )
    orm_obj = SimpleNamespace(
        id=7,
        owner_id=99,
        status=PropertyStatus.AVAILABLE,
        created_at=now,
        updated_at=None,
        owner=owner_obj,
    )
    m = Property.model_validate(orm_obj)
    assert m.id == 7 and m.owner.id == 99 and m.owner.email == "owner@example.com"


# ------------------------- Application & Shortlist -------------------------

def test_application_response_enum_and_from_attributes():
    now = datetime.utcnow()
    orm_obj = SimpleNamespace(
        id=1,
        property_id=2,
        tenant_id=3,
        status=ApplicationStatus.SENT,
        created_at=now,
    )
    m = ApplicationResponse.model_validate(orm_obj)
    assert m.status == ApplicationStatus.SENT and m.property_id == 2


def test_application_update_request_literal_values():
    # valid values
    for v in ["viewed", "accepted", "rejected"]:
        m = ApplicationUpdateRequest(status=v)
        assert m.status == v
    # invalid value
    with pytest.raises(Exception):
        ApplicationUpdateRequest(status="unknown")


def test_application_create_request_required():
    m = ApplicationCreateRequest(property_id=10)
    assert m.property_id == 10
    with pytest.raises(Exception):
        ApplicationCreateRequest()  # type: ignore


def test_shortlist_request_and_response_from_attributes():
    r = ShortlistRequest(property_id=5)
    assert r.property_id == 5

    now = datetime.utcnow()
    orm_obj = SimpleNamespace(id=1, user_id=2, property_id=3, created_at=now)
    resp = ShortlistResponse.model_validate(orm_obj)
    assert resp.id == 1 and resp.created_at == now
