from typing import Annotated

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.schemas import Token
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

DbSession = Annotated[Session, Depends(get_db)]
security = HTTPBearer()
Cred = Annotated[HTTPAuthorizationCredentials, Depends(security)]

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password):
    # Use passlib to hash
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    # Check if password matches hash
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data):
    # Create JWT with expiration
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token):
    # Decode and validate JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(credentials: Cred, db: DbSession) -> User:
    # Extract token from header and verify it
    token = credentials.credentials
    payload = verify_token(token)
    
    # Find user in token or raise 401
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
        
    # Return user
    return user
