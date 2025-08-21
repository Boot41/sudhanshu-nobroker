from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.schemas.schema import UserRegistrationRequest, UserRegistrationResponse, UserLoginRequest, Token
from server.services.auth_service import AuthService
from server.db.database import get_db
from server.api.dependencies import get_current_user
from server.models.model import User

# Create router for auth endpoints
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserRegistrationResponse)
def register_user(user: UserRegistrationRequest, db: Session = Depends(get_db)):
    """
    Register a new user as either tenant or owner
    """
    return AuthService.register_user(user, db)

@auth_router.post("/login", response_model=Token)
def login_for_access_token(user: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return a JWT token
    """
    return AuthService.login_user(user, db)

@auth_router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout the current user. With stateless JWT, logout is client-side (token discard).
    This endpoint exists for symmetry/auditing and to allow future token revocation.
    """
    return {"message": "Logged out"}
