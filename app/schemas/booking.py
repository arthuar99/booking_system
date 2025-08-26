from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.booking import BookingStatus

class BookingCreate(BaseModel):
    service_id: int
    start_at: datetime

class BookingOut(BaseModel):
    id: int
    client_id: int
    freelancer_id: int
    service_id: int
    start_at: datetime
    end_at: datetime
    status: BookingStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)