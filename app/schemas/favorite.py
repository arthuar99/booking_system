# app/schemas/favorite.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FavoriteCreate(BaseModel):
    service_id: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    service_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class FavoriteWithService(BaseModel):
    id: int
    service_id: int
    service_title: Optional[str] = None
    service_price: Optional[float] = None
    created_at: datetime

    class Config:
        orm_mode = True
