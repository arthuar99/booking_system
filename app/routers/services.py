from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.deps import get_current_user
from app.core.roles import require_roles
from app.schemas.service import ServiceCreate, ServiceOut,ServiceUpdate
from app.models.service import Service
from app.models.user import User

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)

# Public route


@router.get("/")
def get_services(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "freelancer"]:
        raise HTTPException(status_code=403, detail="Not authorized to view services")

    return {"message": "Welcome to services!"}



# Public route
@router.get("/{service_id}", response_model=ServiceOut)
def read_service(service_id: int, db: Session = Depends(get_db)):
    svc = db.query(Service).filter(Service.id == service_id).first()
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc


# Freelancer/admin only
@router.post("/", response_model=ServiceOut)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["freelancer", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Only freelancers and admins can create services"
        )

    new_service = Service(
        title=service.title,
        description=service.description,
        price=service.price,
        duration=service.duration,
        freelancer_id=current_user.id,
        created_by_role=current_user.role 
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if current_user.role != "admin":
     raise HTTPException(status_code=403, detail="Only admins can delete services")

    
    db.delete(service)
    db.commit()
    return {"message": f"Service with id {service_id} deleted successfully"}


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    updates: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if current_user.role not in ["admin", "freelancer"]:
        raise HTTPException(status_code=403, detail="Not authorized to update services")
    
     
       # Update service fields
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(service, field, value)


    db.commit()
    db.refresh(service)
    return service


## GET My Bookings
