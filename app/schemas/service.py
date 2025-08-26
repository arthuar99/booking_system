from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ServiceCreate(BaseModel):
    title: str
    description: str | None = None  
    price: float
    duration: int

class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None  
    price: float
    duration: int
    freelancer_id: int
    created_at: datetime

class ServiceUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    duration: int | None = None