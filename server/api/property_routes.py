from fastapi import APIRouter, Depends, status
import re
from sqlalchemy.orm import Session
from typing import List
from server.api.dependencies import get_current_user
from server.db.database import get_db
from server.schemas.schema import (
    PropertyCreate,
    PropertyUpdate,
    Property as PropertyResponse,
    ApplicationUpdateRequest,
    ApplicationResponse,
    ApplicationCreateRequest,
    PropertySearchQuery,
    PropertyDeleteResponse,
    PropertyPublic,
    PropertyOwnerItem,
    PropertyOwnerDetail,
)
from server.services.property_service import PropertyService
from server.models.model import User
from server.services.tenant_service import TenantService

# Create router for property endpoints
property_router = APIRouter(prefix="/properties", tags=["Properties"])
application_router = APIRouter(prefix="/applications", tags=["Applications"])

@property_router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List a new property.
    """
    return PropertyService.create_property(db=db, property_data=property_data, owner_id=current_user.id)

@property_router.get("/", response_model=List[PropertyPublic])
def search_properties(
    filters: PropertySearchQuery = Depends(),
    db: Session = Depends(get_db),
):
    """
    Search properties. Optional filters:
    - city: filter by city (case-insensitive, partial match)
    - max_price: list properties with price <= max_price
    - min_bedrooms: properties with bedrooms >= this value
    - min_area: properties with area_sqft >= this value
    Supports pagination via skip & limit. Public endpoint; no auth required.
    """
    props = PropertyService.search_properties(
        db=db,
        city=filters.city,
        max_price=filters.max_price,
        min_bedrooms=filters.min_bedrooms,
        min_area=filters.min_area,
        skip=filters.skip,
        limit=filters.limit,
    )

    def mask_address(addr: str) -> str:
        # Replace digits with 'x' to hide house numbers/apartment numbers
        return re.sub(r"\d", "x", addr)

    return [
        PropertyPublic(
            name=p.name,
            address=mask_address(p.address or ""),
            city=p.city,
            state=p.state,
            pincode=p.pincode,
            price=p.price,
            bedrooms=p.bedrooms,
            bathrooms=p.bathrooms,
            area_sqft=p.area_sqft,
            description=p.description,
        )
        for p in props
    ]

@property_router.get("/mine", response_model=List[PropertyOwnerItem])
def get_my_properties(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return properties listed by the current owner."""
    props = PropertyService.get_properties_by_owner(db=db, owner_id=current_user.id)
    return [
        PropertyOwnerItem(
            id=p.id,
            name=p.name,
            city=p.city,
            state=p.state,
            price=p.price,
            bedrooms=p.bedrooms,
            bathrooms=p.bathrooms,
            area_sqft=p.area_sqft,
        )
        for p in props
    ]

@property_router.get("/{property_id}/mine", response_model=PropertyOwnerDetail)
def get_my_property_details(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return full details for a property owned by the current user (unmasked)."""
    p = PropertyService.get_property_by_id(db=db, property_id=property_id)
    if p.owner_id != current_user.id:
        # Hide whether the property exists if not owner
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can view only your own properties")

    return PropertyOwnerDetail(
        id=p.id,
        name=p.name,
        address=p.address,
        city=p.city,
        state=p.state,
        pincode=p.pincode,
        price=p.price,
        bedrooms=p.bedrooms,
        bathrooms=p.bathrooms,
        area_sqft=p.area_sqft,
        description=p.description,
        status=p.status,
        owner_id=p.owner_id,
        created_at=p.created_at,
        updated_at=p.updated_at,
    )

@property_router.get("/{property_id}", response_model=PropertyPublic)
def get_property_details(
    property_id: int,
    db: Session = Depends(get_db),
):
    """Get all the information about a single property (public-safe)."""
    p = PropertyService.get_property_by_id(db=db, property_id=property_id)

    def mask_address(addr: str) -> str:
        return re.sub(r"\d", "x", addr)

    return PropertyPublic(
        name=p.name,
        address=mask_address(p.address or ""),
        city=p.city,
        state=p.state,
        pincode=p.pincode,
        price=p.price,
        bedrooms=p.bedrooms,
        bathrooms=p.bathrooms,
        area_sqft=p.area_sqft,
        description=p.description,
    )

@property_router.put("/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    updates: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing property. Only the owner of the property may update it."""
    return PropertyService.update_property(db=db, property_id=property_id, owner_id=current_user.id, updates=updates)

@application_router.put("/{application_id}", response_model=ApplicationResponse)
def manage_application(
    application_id: int,
    payload: ApplicationUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Owners can mark an application as viewed/accepted/rejected for their own properties."""
    return PropertyService.manage_application(
        db=db,
        application_id=application_id,
        owner_id=current_user.id,
        payload=payload,
    )

@application_router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_for_property(
    payload: ApplicationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Tenants can submit an application to rent a property."""
    return TenantService.apply_for_property(db=db, tenant_id=current_user.id, property_id=payload.property_id)

@application_router.get("/", response_model=List[ApplicationResponse])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Tenants can see the status of their applications."""
    return TenantService.get_my_applications(db=db, tenant_id=current_user.id)

@property_router.delete("/{property_id}", response_model=PropertyDeleteResponse)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_id = PropertyService.delete_property(db=db, property_id=property_id, owner_id=current_user.id)
    return PropertyDeleteResponse(id=deleted_id, message="Property deleted successfully")
