from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from server.db.database import Base
import enum

class UserType(enum.Enum):
    TENANT = "tenant"
    OWNER = "owner"

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
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, user_type={self.user_type})>"
