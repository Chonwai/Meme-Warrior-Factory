from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from eth_account.messages import encode_defunct
from web3 import Web3
import secrets
import string

from app.config.settings import settings
from app.config.database import get_db
from app.models.user import User
from app.schemas.user import TokenData

# Make token optional for test mode
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
web3 = Web3()

def generate_nonce(length=32):
    """Generate a random nonce for wallet authentication"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_signature(wallet_address: str, signature: str, message: str) -> bool:
    """Verify a wallet signature against a message"""
    try:
        message_encoded = encode_defunct(text=message)
        recovered_address = web3.eth.account.recover_message(message_encoded, signature=signature)
        return recovered_address.lower() == wallet_address.lower()
    except Exception:
        return False

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme), 
    db: Session = Depends(get_db),
    test_mode: bool = Query(False, description="Set to true to bypass authentication for testing")
):
    """Get the current authenticated user or None in test mode
    
    If test_mode is True and no token is provided, this function will return None
    instead of raising an exception. This allows endpoints to implement their own
    test user logic.
    """
    # If we're in test mode and no token is provided, return None
    # This allows endpoints to implement their own test user logic
    if test_mode and not token:
        return None
    
    # Regular authentication flow
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # If no token and not in test mode, raise exception
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        wallet_address: str = payload.get("sub")
        if wallet_address is None:
            raise credentials_exception
        token_data = TokenData(wallet_address=wallet_address)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.wallet_address == token_data.wallet_address).first()
    if user is None:
        raise credentials_exception
    return user 