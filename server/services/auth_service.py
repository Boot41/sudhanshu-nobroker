from datetime import datetime
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from server.db.database import get_db
from server.models.model import User, UserType
from server.schemas.schema import UserRegistrationRequest, UserRegistrationResponse, UserLoginRequest
from server.core.security import get_password_hash, verify_password, create_access_token

class AuthService:
    @staticmethod
    def register_user(user_data: UserRegistrationRequest, db: Session) -> UserRegistrationResponse:
        """
        Register a new user with validation and business logic
        """
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail="User with this email already exists"
            )
        
        # Hash password using bcrypt
        password_hash = get_password_hash(user_data.password)
        
        # Create new user
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=password_hash,
            user_type=UserType.TENANT if user_data.user_type == "tenant" else UserType.OWNER
        )
        
        try:
            # Save to database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Return response
            return UserRegistrationResponse(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email,
                phone=new_user.phone,
                user_type=new_user.user_type.value,
                message="User registered successfully",
                created_at=new_user.created_at
            )
            
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Internal server error during registration"
            )
    
    @staticmethod
    def login_user(user_data: UserLoginRequest, db: Session):
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": user.email}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    @staticmethod
    def get_all_users(db: Session):
        """Get all registered users (for debugging)"""
        return db.query(User).all()
    
    @staticmethod
    def get_user_by_email(email: str, db: Session):
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
