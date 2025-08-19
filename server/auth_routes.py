from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema import UserRegistrationRequest, UserRegistrationResponse, UserLoginRequest, Token
from usecases.auth_service import AuthService
from database import get_db

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
