from sqlalchemy.orm import Session
from app.database.connection import SessionLocal

# Dependency علشان نقدر نستخدم DB في الـ routers
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
