from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

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
