from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from server.models.model import User, UserType, Property, ShortlistedProperty, Application
from server.schemas.schema import ShortlistRequest

class TenantService:
    @staticmethod
    def shortlist_property(db: Session, tenant_id: int, payload: ShortlistRequest) -> ShortlistedProperty:
        # Validate user is tenant
        tenant = db.query(User).filter(User.id == tenant_id).first()
        if not tenant or tenant.user_type != UserType.TENANT:
            raise HTTPException(status_code=403, detail="Only tenants can shortlist properties")

        # Validate property exists
        prop = db.query(Property).filter(Property.id == payload.property_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")

        # Prevent duplicates
        existing = (
            db.query(ShortlistedProperty)
            .filter(
                ShortlistedProperty.user_id == tenant_id,
                ShortlistedProperty.property_id == payload.property_id,
            )
            .first()
        )
        if existing:
            return existing

        # Create shortlist entry
        entry = ShortlistedProperty(user_id=tenant_id, property_id=payload.property_id)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_shortlisted_properties(db: Session, tenant_id: int) -> List[Property]:
        # Validate user is tenant
        tenant = db.query(User).filter(User.id == tenant_id).first()
        if not tenant or tenant.user_type != UserType.TENANT:
            raise HTTPException(status_code=403, detail="Only tenants can view their shortlist")

        # Join shortlist with properties and return property list
        shortlist_entries = (
            db.query(Property)
            .join(ShortlistedProperty, ShortlistedProperty.property_id == Property.id)
            .filter(ShortlistedProperty.user_id == tenant_id)
            .all()
        )
        return shortlist_entries

    @staticmethod
    def remove_shortlisted_property(db: Session, tenant_id: int, property_id: int) -> None:
        # Validate user is tenant
        tenant = db.query(User).filter(User.id == tenant_id).first()
        if not tenant or tenant.user_type != UserType.TENANT:
            raise HTTPException(status_code=403, detail="Only tenants can modify their shortlist")

        # Find shortlist entry
        entry = (
            db.query(ShortlistedProperty)
            .filter(
                ShortlistedProperty.user_id == tenant_id,
                ShortlistedProperty.property_id == property_id,
            )
            .first()
        )

        if not entry:
            raise HTTPException(status_code=404, detail="Shortlisted property not found")

        db.delete(entry)
        db.commit()
        return None

    @staticmethod
    def apply_for_property(db: Session, tenant_id: int, property_id: int) -> Application:
        # Validate user is tenant
        tenant = db.query(User).filter(User.id == tenant_id).first()
        if not tenant or tenant.user_type != UserType.TENANT:
            raise HTTPException(status_code=403, detail="Only tenants can apply for properties")

        # Validate property exists
        prop = db.query(Property).filter(Property.id == property_id).first()
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found")

        # Prevent tenant from applying to own property
        if prop.owner_id == tenant_id:
            raise HTTPException(status_code=400, detail="Cannot apply to your own property")

        # Prevent duplicate applications by same tenant for same property
        existing = (
            db.query(Application)
            .filter(Application.property_id == property_id, Application.tenant_id == tenant_id)
            .first()
        )
        if existing:
            return existing

        application = Application(property_id=property_id, tenant_id=tenant_id)
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def get_my_applications(db: Session, tenant_id: int) -> List[Application]:
        # Validate user is tenant
        tenant = db.query(User).filter(User.id == tenant_id).first()
        if not tenant or tenant.user_type != UserType.TENANT:
            raise HTTPException(status_code=403, detail="Only tenants can view their applications")

        apps = (
            db.query(Application)
            .filter(Application.tenant_id == tenant_id)
            .order_by(Application.created_at.desc())
            .all()
        )
        return apps
