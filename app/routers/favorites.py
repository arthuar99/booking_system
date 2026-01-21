# app/routers/favorites.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.favorite import Favorite
from app.models.service import Service
from app.schemas.favorite import FavoriteCreate, FavoriteResponse, FavoriteWithService
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a service to user's favorites"""
    # Check if service exists
    service = db.query(Service).filter(Service.id == favorite.service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Check if already favorited
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.service_id == favorite.service_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service already in favorites"
        )
    
    new_favorite = Favorite(
        user_id=current_user.id,
        service_id=favorite.service_id
    )
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    
    return new_favorite


@router.get("/", response_model=List[FavoriteWithService])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all favorite services for the current user"""
    favorites = db.query(Favorite).filter(Favorite.user_id == current_user.id).all()
    
    result = []
    for fav in favorites:
        service = db.query(Service).filter(Service.id == fav.service_id).first()
        result.append(FavoriteWithService(
            id=fav.id,
            service_id=fav.service_id,
            service_title=service.title if service else None,
            service_price=service.price if service else None,
            created_at=fav.created_at
        ))
    
    return result


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a service from user's favorites"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.service_id == service_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    db.delete(favorite)
    db.commit()
    
    return None


@router.get("/check/{service_id}")
def check_favorite(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check if a service is in user's favorites"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.service_id == service_id
    ).first()
    
    return {"is_favorite": favorite is not None}
