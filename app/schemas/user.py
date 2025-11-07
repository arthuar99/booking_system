from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    freelancer = "freelancer"
    client = "client"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.client

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
