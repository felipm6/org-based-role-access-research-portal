from fastapi import Depends, HTTPException, status

from src.models.database import User, UserRole
from .auth import get_current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require ADMIN role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


def require_coordinator_or_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Require STUDY_COORDINATOR or ADMIN role."""
    if current_user.role not in [UserRole.STUDY_COORDINATOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Study Coordinator or Admin access required",
        )
    return current_user
