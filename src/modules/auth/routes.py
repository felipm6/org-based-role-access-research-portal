from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.connection import get_db
from src.models.database import User
from src.modules.auth.schemas import LoginRequest, TokenResponse
from src.modules.auth.auth_services import verify_secret, create_access_token
from src.modules.auth.swagger import AUTH_RESPONSES

router = APIRouter(tags=["Authentication"])


@router.post("/auth", response_model=TokenResponse, responses=AUTH_RESPONSES)
async def authenticate(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user with client_id and client_secret.
    Returns a Bearer token for API access.
    """
    user = db.query(User).filter(User.client_id == login_data.client_id).first()

    # Check if user exists and secret is correct
    if not user or not verify_secret(login_data.client_secret, user.client_secret_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    # Create Bearer token
    access_token = create_access_token(
        data={
            "sub": str(user.id),  # Standard JWT field for user ID
            "client_id": user.client_id,
            "role": user.role.value,
        }
    )

    return TokenResponse(access_token=access_token)
