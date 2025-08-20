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
    PropertyDeleteResponse,
)
from server.services.property_service import PropertyService
from server.models.model import User

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
def get_all_properties(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get a list of all available properties.
    """
    return PropertyService.get_all_properties(db=db, skip=skip, limit=limit)

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

@property_router.delete("/{property_id}", response_model=PropertyDeleteResponse)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_id = PropertyService.delete_property(db=db, property_id=property_id, owner_id=current_user.id)
    return PropertyDeleteResponse(id=deleted_id, message="Property deleted successfully")
