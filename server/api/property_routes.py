from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from server.api.dependencies import get_current_user
from server.db.database import get_db
from server.schemas.schema import PropertyCreate, Property as PropertyResponse
from server.services.property_service import PropertyService
from server.models.model import User

# Create router for property endpoints
property_router = APIRouter(prefix="/properties", tags=["Properties"])

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
