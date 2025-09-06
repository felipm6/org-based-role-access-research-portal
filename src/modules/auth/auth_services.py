import bcrypt
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from configuration.configuration import get_settings
from src.constants import SECRET_KEY

settings = get_settings()
security = HTTPBearer()


def verify_secret(secret: str, hashed: str) -> bool:
    """Verify a secret against its hash"""
    return bcrypt.checkpw(secret.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict):
    """Create JWT access token with configured expiration time"""
    algorithm = settings.jwt.algorithm
    expiration = settings.jwt.expiration
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.jwt.algorithm])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
