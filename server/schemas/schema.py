from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime
from server.models.model import PropertyStatus, ApplicationStatus

class UserRegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    user_type: Literal["tenant", "owner"]

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    user_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserRegistrationResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    user_type: str
    message: str
    created_at: datetime

class ErrorResponse(BaseModel):
    error: str
    detail: str

# Profile (GET /users/me)
class UserMeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    user_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserMeUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Property Schemas
class PropertyBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    pincode: str
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: int
    description: Optional[str] = None

class PropertyCreate(PropertyBase):
    pass

class Property(BaseModel):
    id: int
    owner_id: int
    status: PropertyStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner: UserResponse

    class Config:
        from_attributes = True

# Update payload for properties (all fields optional)
class PropertyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area_sqft: Optional[int] = None
    description: Optional[str] = None

class PropertySearchQuery(BaseModel):
    # Optional filters for GET /properties
    city: Optional[str] = None
    max_price: Optional[float] = None
    skip: int = 0
    limit: int = 100

class PropertyDeleteResponse(BaseModel):
    id: int
    message: str

class PropertyPublic(BaseModel):
    # Public-safe property details
    name: str
    address: str  # should be masked by the service before returning
    city: str
    state: str
    pincode: str
    price: float
    bedrooms: int
    bathrooms: int
    area_sqft: int
    description: Optional[str] = None

# Application Schemas
class ApplicationResponse(BaseModel):
    id: int
    property_id: int
    tenant_id: int
    status: ApplicationStatus
    created_at: datetime

    class Config:
        from_attributes = True

class ApplicationUpdateRequest(BaseModel):
    # Owners can mark as viewed, accepted, or rejected
    status: Literal["viewed", "accepted", "rejected"]

class ApplicationCreateRequest(BaseModel):
    # Tenants apply to a property
    property_id: int

# Shortlist Schemas
class ShortlistRequest(BaseModel):
    property_id: int

class ShortlistResponse(BaseModel):
    id: int
    user_id: int
    property_id: int
    created_at: datetime

    class Config:
        from_attributes = True
