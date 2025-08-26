from pydantic import BaseModel, conint
from datetime import time

class AvailabilityCreate(BaseModel):
    day_of_week: conint(ge=0, le=6)  # 0=Monday, 6=Sunday
    start_time: time
    end_time: time

class AvailabilityOut(AvailabilityCreate):
    id: int
    freelancer_id: int

    class Config:
        orm_mode = True
