from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.api.dependencies import get_current_user
from server.db.database import get_db
from server.models.model import User
from server.schemas.schema import UserMeResponse, UserMeUpdateRequest
from server.services.registereduser_service import RegisteredUserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserMeResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RegisteredUserService.get_me(db, current_user)

@router.put("/me", response_model=UserMeResponse)
def update_my_profile(
    payload: UserMeUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return RegisteredUserService.update_me(db, current_user, payload)
