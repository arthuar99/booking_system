from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models import booking as models, service as service_models
from app.schemas.booking import BookingCreate, BookingOut
from app.core.deps import get_current_user
from app.models.user import User
from datetime import timedelta
from app.models.booking import Booking, BookingStatus 
from app.core.jwt_bearer import jwt_bearer

router = APIRouter(
    prefix= "/bookings",
    tags=["Bookings"]
)

@router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(booking_data: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can create bookings")
    
    # Get the service first
    service = db.query(service_models.Service).filter(service_models.Service.id == booking_data.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Calculate end_at from duration
    end_time = booking_data.start_at + timedelta(minutes=service.duration)

    new_booking = models.Booking(
    client_id=current_user.id,
    freelancer_id=service.freelancer_id,
    service_id=booking_data.service_id,
    start_at=booking_data.start_at,
    end_at=end_time,
    status=BookingStatus.pending  
)

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

##GET My Bookings

@router.get("/" , response_model=list[BookingOut])
def get_my_bookings(
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    query_map = {
        "client": lambda: db.query(Booking).filter(Booking.client_id == current_user.id).all(),
        "freelancer": lambda: db.query(Booking).filter(Booking.freelancer_id == current_user.id).all(),
        "admin": lambda: db.query(Booking).all()
    }

    if current_user.role not in query_map:
         raise HTTPException(status_code=403, detail="Not authorized to view bookings")
    
    return query_map[current_user.role]()
    

    ## put booking status

@router.put("/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    try:
        status_enum = BookingStatus(new_status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

    
    status_permissions_map = {
        "canceled": lambda user, b: user.role == "client" and b.client_id == user.id,
        "confirmed": lambda user, b: user.role == "freelancer" and b.freelancer_id == user.id,
        "completed": lambda user, b: user.role in {"admin", "freelancer"},
    }

    check_permission = status_permissions_map.get(new_status)
    if check_permission and not check_permission(current_user, booking):
        raise HTTPException(status_code=403, detail=f"You are not allowed to mark this booking as {new_status}")

    booking.status = status_enum
    db.commit()
    db.refresh(booking)
    return booking


## delete with query map

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    delete_permissions_map = {
        "client": lambda user, b: b.client_id == user.id,
        "freelancer": lambda user, b: b.freelancer_id == user.id,
        "admin": lambda user, b: True,
    }

    check_permission = delete_permissions_map.get(current_user.role)
    if not check_permission or not check_permission(current_user, booking):
        raise HTTPException(status_code=403, detail="You are not authorized to delete this booking")

    db.delete(booking)
    db.commit()


# Admin-only status update (PATCH)
@router.patch("/{booking_id}/status")
def admin_update_booking_status(
    booking_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    try:
        status_enum = BookingStatus(new_status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")

    booking.status = status_enum
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/protected", dependencies=[Depends(jwt_bearer)])
def protected_route():
    return {"message": "You have access to this route"}

