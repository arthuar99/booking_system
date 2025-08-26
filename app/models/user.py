from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database.connection import Base
import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum

class UserRole(str, enum.Enum):
    freelancer = "freelancer"
    client = "client"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole, name="userrole_enum"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    services = relationship("Service", back_populates="freelancer") 
