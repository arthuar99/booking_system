# ✅ app/core/deps.py

from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.database.session import get_db
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import time

# ----------------------------
# Token Configuration
# ----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Matches your route

# ----------------------------
# Get Current User Dependency
# ----------------------------
def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    # Check for token in cookies if not provided in Authorization header
    if not token:
        token = request.cookies.get("access_token")
        if not token:
            raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        exp: int = payload.get("exp")

        # Validate expiration
        if exp and exp < int(time.time()):
            raise credentials_exception

        if user_id is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def freelancer_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "freelancer":
        raise HTTPException(status_code=403, detail="Freelancer access required")
    return current_user

def role_required(allowed_roles: list[str]):
    def role_dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied: insufficient permissions")
        return current_user
    return role_dependency

# --------------------------------------
# Try get current user (no exception)
# --------------------------------------
def try_get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """Best-effort decode of Authorization Bearer token; returns None on failure.

    Useful for server-rendered page routes where we want to redirect rather than
    return a 401 JSON error response.
    """
    auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        return None
    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            return None
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user
    except JWTError:
        return None
