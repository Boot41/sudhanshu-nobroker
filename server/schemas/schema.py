from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime
from server.models.model import PropertyStatus

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

class Property(PropertyBase):
    id: int
    owner_id: int
    status: PropertyStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner: UserResponse

    class Config:
        from_attributes = True
