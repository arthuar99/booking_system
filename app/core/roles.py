from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_user
from app.models.user import User

def require_roles(allowed_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )
    return role_checker
