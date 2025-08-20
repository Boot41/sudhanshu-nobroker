from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from server.models.model import User, UserType, Property, Application, ApplicationStatus
from server.schemas.schema import PropertyCreate, PropertyUpdate, ApplicationUpdateRequest

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

    @staticmethod
    def get_all_properties(db: Session, skip: int = 0, limit: int = 100) -> List[Property]:
        """Retrieve all properties with pagination."""
        return db.query(Property).offset(skip).limit(limit).all()

    @staticmethod
    def search_properties(
        db: Session,
        city: str | None = None,
        max_price: float | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Property]:
        """Search properties optionally filtering by city and max_price with pagination."""
        query = db.query(Property)
        if city:
            query = query.filter(Property.city.ilike(f"%{city}%"))
        if max_price is not None:
            query = query.filter(Property.price <= max_price)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_property(db: Session, property_id: int, owner_id: int, updates: PropertyUpdate) -> Property:
        """Update an existing property if the current user is the owner."""
        prop = db.query(Property).filter(Property.id == property_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")

        if prop.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="You can only update your own properties")

        # Apply updates only for provided fields; ignore nulls
        data = updates.dict(exclude_unset=True, exclude_none=True)
        if not data:
            raise HTTPException(status_code=400, detail="No fields provided to update")
        for key, value in data.items():
            setattr(prop, key, value)

        db.add(prop)
        db.commit()
        db.refresh(prop)
        return prop

    @staticmethod
    def manage_application(
        db: Session,
        application_id: int,
        owner_id: int,
        payload: ApplicationUpdateRequest,
    ) -> Application:
        """Allow property owners to update status of applications for their properties."""
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        # Ensure the application belongs to a property owned by the current user
        prop = db.query(Property).filter(Property.id == application.property_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found for application")
        if prop.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="You can manage applications only for your own properties")

        # Only allow transitions to viewed/accepted/rejected
        new_status_map = {
            "viewed": ApplicationStatus.VIEWED,
            "accepted": ApplicationStatus.ACCEPTED,
            "rejected": ApplicationStatus.REJECTED,
        }
        application.status = new_status_map[payload.status]

        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def delete_property(db: Session, property_id: int, owner_id: int) -> int:
        """Delete a property owned by the current user. Also clean up related applications."""
        prop = db.query(Property).filter(Property.id == property_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")
        if prop.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="You can delete only your own properties")

        # Delete related applications first (no cascade configured)
        db.query(Application).filter(Application.property_id == property_id).delete(synchronize_session=False)

        # Now delete the property
        db.delete(prop)
        db.commit()
        return property_id
