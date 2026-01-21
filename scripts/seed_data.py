#!/usr/bin/env python3
"""
Seed data script for CI testing.
Creates sample users, services, and bookings for testing.
"""

import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.service import Service
from app.models.booking import Booking, BookingStatus
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def seed_data():
    """Seed the database with test data."""
    db: Session = SessionLocal()
    
    try:
        # Check if data already exists
        existing_user = db.query(User).first()
        if existing_user:
            print("Database already contains data. Skipping seed.")
            return
        
        print("Seeding database with test data...")
        
        # Create users
        freelancer = User(
            username="test_freelancer",
            email="freelancer@test.com",
            password=hash_password("password123"),
            role=UserRole.freelancer
        )
        
        client = User(
            username="test_client",
            email="client@test.com",
            password=hash_password("password123"),
            role=UserRole.client
        )
        
        admin = User(
            username="test_admin",
            email="admin@test.com",
            password=hash_password("admin123"),
            role=UserRole.admin
        )
        
        db.add_all([freelancer, client, admin])
        db.commit()
        db.refresh(freelancer)
        db.refresh(client)
        print(f"Created {3} users")
        
        # Create services
        service1 = Service(
            freelancer_id=freelancer.id,
            title="Web Development",
            description="Full-stack web development service including frontend and backend.",
            price=150.0,
            duration=60,  # 60 minutes
            created_by_role=UserRole.freelancer
        )
        
        service2 = Service(
            freelancer_id=freelancer.id,
            title="UI/UX Design",
            description="Professional UI/UX design service for web and mobile applications.",
            price=100.0,
            duration=45,  # 45 minutes
            created_by_role=UserRole.freelancer
        )
        
        db.add_all([service1, service2])
        db.commit()
        db.refresh(service1)
        print(f"Created {2} services")
        
        # Create a sample booking
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(minutes=60)
        
        booking = Booking(
            client_id=client.id,
            freelancer_id=freelancer.id,
            service_id=service1.id,
            start_at=start_time,
            end_at=end_time,
            status=BookingStatus.pending
        )
        
        db.add(booking)
        db.commit()
        print(f"Created 1 booking")
        
        print("✓ Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
