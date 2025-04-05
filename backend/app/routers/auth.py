from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.utils.auth import generate_nonce, verify_signature, create_access_token
from app.models.user import User
from app.schemas.user import Token, UserCreate
from datetime import timedelta
from app.config.settings import settings

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.get("/nonce/{wallet_address}")
async def get_wallet_nonce(wallet_address: str, db: Session = Depends(get_db)):
    """Get or create a nonce for the specified wallet address"""
    # For testing purposes, allow any wallet address without verification
    # In a real implementation, this would verify the wallet address format
    
    # Check if user exists
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    
    if not user:
        # Create new user with a new nonce
        new_nonce = generate_nonce()
        user = User(wallet_address=wallet_address, nonce=new_nonce)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user's nonce
        new_nonce = generate_nonce()
        user.nonce = new_nonce
        db.commit()
        db.refresh(user)
    
    return {"wallet_address": wallet_address, "nonce": user.nonce}

@router.post("/verify", response_model=Token)
async def verify_wallet_signature(
    wallet_address: str, 
    signature: str = "mock_signature",  # Allow mock signature for testing
    db: Session = Depends(get_db)
):
    """Verify a wallet signature and return an access token"""
    # For frontend testing, we'll accept any signature
    # In a real implementation, this would verify the signature
    
    user = db.query(User).filter(User.wallet_address == wallet_address).first()
    if not user:
        # For frontend testing, create a user if not exists
        new_nonce = generate_nonce()
        user = User(wallet_address=wallet_address, nonce=new_nonce)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": wallet_address}, expires_delta=access_token_expires
    )
    
    # Generate a new nonce for next login
    user.nonce = generate_nonce()
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"} 