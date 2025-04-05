from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=dict)
async def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user information (placeholder)"""
    # For testing, we'll add some mock data
    mock_stats = {
        "total_soldiers": 5,
        "deployed_soldiers": 2,
        "battles_participated": 8,
        "battles_won": 3,
        "total_votes_received": 240,
        "reward_tokens_earned": 350
    }
    
    return {
        "success": True,
        "user": {
            "id": current_user.id,
            "wallet_address": current_user.wallet_address,
            "joined": current_user.created_at,
            "stats": mock_stats
        }
    }

@router.get("/leaderboard", response_model=dict)
async def get_leaderboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user leaderboard (placeholder)"""
    # For testing, return mock leaderboard data
    mock_leaderboard = [
        {
            "rank": 1,
            "wallet_address": "0x1234...abcd",
            "soldiers_count": 12,
            "battles_won": 15,
            "total_votes": 720,
            "reward_tokens": 1450
        },
        {
            "rank": 2,
            "wallet_address": "0x5678...efgh",
            "soldiers_count": 8,
            "battles_won": 10,
            "total_votes": 550,
            "reward_tokens": 950
        },
        {
            "rank": 3,
            "wallet_address": "0x90ab...ijkl",
            "soldiers_count": 6,
            "battles_won": 7,
            "total_votes": 410,
            "reward_tokens": 650
        },
        # Add the current user's position
        {
            "rank": 7,
            "wallet_address": current_user.wallet_address,
            "soldiers_count": 5,
            "battles_won": 3,
            "total_votes": 240,
            "reward_tokens": 350,
            "is_current_user": True
        }
    ]
    
    return {
        "success": True,
        "leaderboard": mock_leaderboard
    } 