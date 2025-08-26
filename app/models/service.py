from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base
from sqlalchemy import Enum
from app.core.enums import UserRole 


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer,primary_key=True, index=True)
    freelancer_id = Column(Integer, ForeignKey("users.id" , ondelete="CASCADE"),nullable=False)
    title  =Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False) 
    created_by_role = Column(Enum(UserRole, name="userrole_enum"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    freelancer = relationship("User", back_populates= "services")
    
