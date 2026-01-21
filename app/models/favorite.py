# app/models/favorite.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Ensure a user can only favorite a service once
    __table_args__ = (
        UniqueConstraint('user_id', 'service_id', name='unique_user_service_favorite'),
    )

    user = relationship("User", backref="favorites")
    service = relationship("Service", backref="favorited_by")
