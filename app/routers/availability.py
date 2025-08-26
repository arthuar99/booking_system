from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.availability import AvailabilitySlot
from app.schemas.availability import AvailabilityCreate, AvailabilityOut
from app.models.user import User
from app.models.review import Review

from app.core.deps import get_current_user
from app.schemas.review import ReviewCreate, ReviewOut


router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)

@router.post("/" ,  response_model=AvailabilityOut , status_code=status.HTTP_201_CREATED)
def create_slot(
    slot:AvailabilityCreate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    if current_user.role != "freelancer":
         raise HTTPException(status_code=403, detail="Only freelancers can create availability slots")
    
    new_slot = AvailabilitySlot(
         **slot.dict(),
         freelancer_id = current_user.id
    )

    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot


@router.get("/", response_model=list[AvailabilityOut])
def get_my_slots(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "freelancer":
        raise HTTPException(status_code=403, detail="Only freelancers can view their slots")

    return db.query(AvailabilitySlot).filter_by(freelancer_id=current_user.id).all()


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(slot_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    slot = db.query(AvailabilitySlot).filter_by(id=slot_id, freelancer_id=current_user.id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found or unauthorized")

    db.delete(slot)
    db.commit()
    