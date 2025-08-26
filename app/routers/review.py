from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.deps import get_current_user
from app.models import Review, Booking, User
from app.schemas.review import ReviewCreate, ReviewOut

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def get_booking_or_404(db:Session , booking_id:int)->Booking:
    booking= db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

def get_review_or_404(db:Session , review_id : int)->Review:
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

def assert_client_owns_booking(booking:Booking , user:User):
    if booking.client_id != user.id:
        raise HTTPException(status_code=403, detail="You do not own this booking")
    

@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review_data:ReviewCreate,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    booking = get_booking_or_404(db,review_data.booking_id)
    assert_client_owns_booking(booking,current_user)
    if booking.review:
         raise HTTPException(status_code=400, detail="Review already exists for this booking")
    
    review = Review(**review_data.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.get("/", response_model=list[ReviewOut])
def get_all_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return db.query (Review).all()

@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = get_review_or_404(db, review_id)
    assert_client_owns_booking(review.booking, current_user)

    review.rating = review_data.rating
    review.comment = review_data.comment
    db.commit()
    db.refresh(review)
    return review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = get_review_or_404(db, review_id)
    assert_client_owns_booking(review.booking, current_user)

    db.delete(review)
    db.commit()

    