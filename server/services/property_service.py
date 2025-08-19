from fastapi import HTTPException
from sqlalchemy.orm import Session
from server.models.model import User, UserType, Property
from server.schemas.schema import PropertyCreate

class PropertyService:
    @staticmethod
    def create_property(db: Session, property_data: PropertyCreate, owner_id: int) -> Property:
        # Check if the user is an owner
        owner = db.query(User).filter(User.id == owner_id).first()
        if not owner or owner.user_type != UserType.OWNER:
            raise HTTPException(
                status_code=403,
                detail="Only owners can list a new property"
            )

        # Create a new property instance
        new_property = Property(
            **property_data.dict(),
            owner_id=owner_id
        )

        # Add to the database
        db.add(new_property)
        db.commit()
        db.refresh(new_property)

        return new_property
