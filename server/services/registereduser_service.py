from sqlalchemy.orm import Session
from server.models.model import User
from server.schemas.schema import UserMeResponse, UserMeUpdateRequest

class RegisteredUserService:
    @staticmethod
    def get_me(db: Session, user: User) -> UserMeResponse:
        # Return the authenticated user's profile
        return UserMeResponse.from_orm(user)

    @staticmethod
    def update_me(db: Session, user: User, payload: UserMeUpdateRequest) -> UserMeResponse:
        # Update allowed fields if provided
        if payload.name is not None:
            user.name = payload.name
        if payload.phone is not None:
            user.phone = payload.phone

        db.add(user)
        db.commit()
        db.refresh(user)
        return UserMeResponse.from_orm(user)
