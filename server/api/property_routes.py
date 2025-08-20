from fastapi import APIRouter, Depends, status
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

@property_router.get("/", response_model=List[PropertyResponse])
def search_properties(
    filters: PropertySearchQuery = Depends(),
    db: Session = Depends(get_db),
):
    """
    Search properties. Optional filters:
    - city: filter by city (case-insensitive, partial match)
    - max_price: list properties with price <= max_price
    Supports pagination via skip & limit. Public endpoint; no auth required.
    """
    return PropertyService.search_properties(
        db=db,
        city=filters.city,
        max_price=filters.max_price,
        skip=filters.skip,
        limit=filters.limit,
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
