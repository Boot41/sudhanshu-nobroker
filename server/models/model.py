from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.db.database import Base
import enum

class UserType(enum.Enum):
    TENANT = "tenant"
    OWNER = "owner"

class PropertyStatus(enum.Enum):
    AVAILABLE = "available"
    RENTED = "rented"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(Enum(UserType, native_enum=False), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    properties = relationship("Property", back_populates="owner")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, user_type={self.user_type})>"

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    area_sqft = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(PropertyStatus, native_enum=False), nullable=False, default=PropertyStatus.AVAILABLE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="properties")

    def __repr__(self):
        return f"<Property(id={self.id}, name={self.name})>"
