from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.connection import get_db
from src.models.database import User as DBUser
from src.guards import get_current_user, require_admin
from .schemas import UserCreate, UserResponse, RoleUpdate
from .user_services import (
    get_users_by_organization,
    create_user_in_organization,
    change_user_role_in_organization,
)

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/", response_model=List[UserResponse])
async def get_users(
    current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    View users based on role:
    - ADMIN: Can see all users in their organization
    - Other roles: Can only see themselves
    """
    if current_user.role.value == "admin":
        return get_users_by_organization(current_user.org_id, db)
    else:
        return [current_user]


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: DBUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Create user in organization (Admin only)

    Creates a new user within the same organization as the authenticated admin.
    Only users with ADMIN role can create new users.
    """
    return create_user_in_organization(user_data, current_user.org_id, db)


@router.put("/{user_id}/role", response_model=UserResponse)
async def change_user_role(
    user_id: str,
    role_data: RoleUpdate,
    current_user: DBUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Change user role (Admin only)

    Admin is the only one able to change the role of another user.
    Can only change roles of users within the same organization.
    """
    return change_user_role_in_organization(
        user_id, role_data.role, current_user.org_id, db
    )
