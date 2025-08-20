from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from server.api.dependencies import get_current_user
from server.db.database import get_db
from server.models.model import User
from server.schemas.schema import ShortlistRequest, ShortlistResponse, Property as PropertyResponse
from server.services.tenant_service import TenantService

router = APIRouter(prefix="/me", tags=["Tenant"])

@router.post("/shortlist", response_model=ShortlistResponse)
def shortlist_property(
    payload: ShortlistRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TenantService.shortlist_property(db=db, tenant_id=current_user.id, payload=payload)

@router.get("/shortlist", response_model=List[PropertyResponse])
def get_shortlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TenantService.get_shortlisted_properties(db=db, tenant_id=current_user.id)
