import enum

class UserRole(str, enum.Enum):
    freelancer = "freelancer"
    client = "client"
    admin = "admin"