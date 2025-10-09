"""
Authentication utilities for user management and JWT tokens.
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import secrets
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simple password hashing for demo (use bcrypt in production)
def simple_hash_password(password: str) -> str:
    """Simple password hashing for demo purposes."""
    salt = "lexsy-ai-demo-salt"  # In production, use random salts
    return hashlib.sha256((password + salt).encode()).hexdigest()

# JWT Bearer token
security = HTTPBearer()

# In-memory user storage (replace with database in production)
fake_users_db = {}

# Initialize demo user from environment variables
def init_demo_user():
    # Get demo credentials from environment variables (for security)
    demo_email = os.getenv("DEMO_USER_EMAIL", "demo@lexsy.ai")
    demo_password = os.getenv("DEMO_USER_PASSWORD", "demo123")
    demo_name = os.getenv("DEMO_USER_NAME", "Demo User")
    
    if demo_email not in fake_users_db:
        fake_users_db[demo_email] = {
            "id": "1",
            "email": demo_email,
            "hashed_password": simple_hash_password(demo_password),
            "full_name": demo_name,
            "is_active": True,
        }

class User(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return simple_hash_password(plain_password) == hashed_password


def get_user(email: str) -> Optional[dict]:
    """Get user from database by email."""
    init_demo_user()  # Ensure demo user exists
    return fake_users_db.get(email)

def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate user with email and password."""
    user = get_user(email)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_user(user_data: UserCreate) -> dict:
    """Create a new user."""
    if user_data.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user_id = str(len(fake_users_db) + 1)
    hashed_password = simple_hash_password(user_data.password)
    
    user = {
        "id": user_id,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "full_name": user_data.full_name,
        "is_active": True,
    }
    
    fake_users_db[user_data.email] = user
    return user

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(email)
    if user is None:
        raise credentials_exception
    
    return User(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        is_active=user["is_active"]
    )
