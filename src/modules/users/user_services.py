import uuid
import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.database import User as DBUser
from .schemas import UserCreate


def get_users_by_organization(org_id: str, db: Session) -> list[DBUser]:
    """Get all users in the same organization"""
    return db.query(DBUser).filter(DBUser.org_id == org_id).all()


def create_user_in_organization(
    user_data: UserCreate, admin_org_id: str, db: Session
) -> DBUser:
    """Create a new user in the admin's organization"""
    # Check if client_id already exists
    existing_user = (
        db.query(DBUser).filter(DBUser.client_id == user_data.client_id).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Client ID already exists")

    # Check if email already exists
    existing_email = db.query(DBUser).filter(DBUser.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the client secret
    hashed_secret = bcrypt.hashpw(
        user_data.client_secret.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    # Create new user
    new_user = DBUser(
        id=str(uuid.uuid4()),
        client_id=user_data.client_id,
        client_secret_hash=hashed_secret,
        email=user_data.email,
        name=user_data.name,
        org_id=admin_org_id,
        role=user_data.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def change_user_role_in_organization(
    user_id: str, new_role, admin_org_id: str, db: Session
) -> DBUser:
    """Change user role within the same organization"""
    # Find the user to modify
    user_to_modify = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user_to_modify:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user belongs to admin's organization
    if user_to_modify.org_id != admin_org_id:
        raise HTTPException(
            status_code=403, detail="Cannot modify users from other organizations"
        )

    # Update the role
    user_to_modify.role = new_role
    db.commit()
    db.refresh(user_to_modify)

    return user_to_modify
