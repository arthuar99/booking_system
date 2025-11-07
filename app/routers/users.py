from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import get_current_user
from app.models.user import User
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserUpdate
from app.core.hash import Hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def read_me(current_user:User= Depends(get_current_user)):
    return{
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role.value,
        "email": current_user.email
    }

@router.put("/me")
def update_profile(payload: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated = False
    # Check username uniqueness
    if payload.username and payload.username != current_user.username:
        exists = db.query(User).filter(User.username == payload.username).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
        current_user.username = payload.username
        updated = True

    # Check email uniqueness
    if payload.email and payload.email != current_user.email:
        exists = db.query(User).filter(User.email == payload.email).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        current_user.email = payload.email
        updated = True

    # Update password if provided
    if payload.password:
        current_user.password = Hash.bcrypt(payload.password)
        updated = True

    if updated:
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    return {"detail": "Profile updated", "user": {"id": current_user.id, "username": current_user.username, "email": current_user.email}}