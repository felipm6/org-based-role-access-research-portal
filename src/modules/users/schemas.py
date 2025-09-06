from pydantic import BaseModel
from src.models.database import UserRole


class UserCreate(BaseModel):
    client_id: str
    client_secret: str
    email: str
    name: str
    role: UserRole


class UserResponse(BaseModel):
    id: str
    client_id: str
    email: str
    name: str
    org_id: str
    role: UserRole

    class Config:
        from_attributes = True


class RoleUpdate(BaseModel):
    role: UserRole
