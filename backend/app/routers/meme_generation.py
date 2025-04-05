from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import time

# Define a router with tags
router = APIRouter(
    prefix="/meme",
    tags=["meme generation"],
)

# Detect if we're running in Vercel
IN_VERCEL = os.environ.get('VERCEL') == '1'

# Only import database dependencies if not in Vercel
if not IN_VERCEL:
    try:
        from app.config.database import get_db
        from app.utils.auth import get_current_user
        from app.models.user import User
        from app.models.meme_soldier import MemeSoldier
        from app.schemas.meme_soldier import MemeSoldierGeneration, MemeSoldierGenerationResponse
    except ImportError as e:
        print(f"Error importing database dependencies: {e}")
else:
    # Define minimal schemas for Vercel
    from pydantic import BaseModel
    
    class MemeSoldierGeneration(BaseModel):
        prompt: str

# Import AI utilities which should work in both environments
from app.utils.ai import generate_meme_image, generate_meme_soldier_name

@router.post("/generate", response_model=dict)
async def generate_meme(
    request: MemeSoldierGeneration,
    db: Session = None,
    current_user: Optional[object] = None,
    test_mode: bool = Query(False, description="Set to true to bypass authentication (for frontend testing)")
):
    """Generate meme images and names based on a prompt
    
    This endpoint will:
    1. Parse the user prompt to identify 2 distinct items or themes
    2. Generate a pixel art meme image for each item
    3. Generate a name for each meme soldier
    4. Return the results as a list of items
    
    If test_mode is True, authentication will be bypassed.
    """
    try:
        # For Vercel environment, use simplified flow without DB
        if IN_VERCEL:
            # Generate the meme images
            image_result = generate_meme_image(request.prompt)
            
            if not image_result["success"]:
                # Return error instead of raising exception
                return {
                    "success": False,
                    "error": image_result.get("error", "Failed to generate images")
                }
                
            # Generate names for each item
            result_items = []
            for item in image_result["items"]:
                # Generate a name for this meme soldier
                name = generate_meme_soldier_name(item["prompt"])
                
                result_items.append({
                    "id": 999,  # Dummy ID for Vercel
                    "name": name,
                    "prompt": item["prompt"],
                    "image_url": item["image_url"],
                    "coin_icon_url": item["coin_icon_url"]
                })
            
            return {
                "success": True,
                "items": result_items
            }
            
        # For non-Vercel environments with database
        # For testing mode, use a default user if no authentication provided
        if test_mode and not current_user:
            # Get or create a test user
            test_wallet = "0xTEST1234567890abcdef1234567890abcdef12345678"
            test_user = db.query(User).filter(User.wallet_address == test_wallet).first()
            
            if not test_user:
                # Create a test user
                from app.utils.auth import generate_nonce
                test_user = User(
                    wallet_address=test_wallet,
                    nonce=generate_nonce(),
                    is_active=True
                )
                db.add(test_user)
                db.commit()
                db.refresh(test_user)
            
            current_user = test_user
        
        # Regular authentication check for non-test mode
        if not test_mode and not current_user:
            return {
                "success": False,
                "error": "Authentication required"
            }
        
        # Generate the meme images
        image_result = generate_meme_image(request.prompt)
        
        if not image_result["success"]:
            return {
                "success": False,
                "error": image_result.get("error", "Failed to generate images")
            }
            
        # Generate names and create records for each item
        result_items = []
        for item in image_result["items"]:
            # Generate a name for this meme soldier
            name = generate_meme_soldier_name(item["prompt"])
            
            # Create a database record for this meme soldier
            meme_soldier = MemeSoldier(
                owner_id=current_user.id,
                name=name,
                prompt=item["prompt"],
                image_url=item["image_url"],
                coin_icon_url=item["coin_icon_url"],
                deployed_to_battlefield=False,
                token_amount=0,  # Will be set when minted
                token_amount_deployed=0
            )
            
            db.add(meme_soldier)
            db.commit()
            db.refresh(meme_soldier)
            
            result_items.append({
                "id": meme_soldier.id,
                "name": meme_soldier.name,
                "prompt": meme_soldier.prompt,
                "image_url": meme_soldier.image_url,
                "coin_icon_url": meme_soldier.coin_icon_url
            })
        
        return {
            "success": True,
            "items": result_items
        }
    except Exception as e:
        if db:
            db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@router.post("/generate_test", response_model=dict)
async def generate_meme_test(
    request: MemeSoldierGeneration
):
    """Test endpoint to generate meme images without authentication or database storage
    
    This endpoint is intended for frontend testing only.
    """
    try:
        # Generate the meme images
        image_result = generate_meme_image(request.prompt)
        
        if not image_result["success"]:
            return {
                "success": False,
                "error": image_result.get("error", "Failed to generate images")
            }
            
        # Generate names for each item
        result_items = []
        for item in image_result["items"]:
            # Generate a name for this meme soldier
            name = generate_meme_soldier_name(item["prompt"])
            
            result_items.append({
                "id": 999,  # Dummy ID
                "name": name,
                "prompt": item["prompt"],
                "image_url": item["image_url"],
                "coin_icon_url": item["coin_icon_url"]
            })
        
        return {
            "success": True,
            "items": result_items
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Only include this endpoint if not in Vercel
if not IN_VERCEL:
    @router.post("/mint/{soldier_id}", response_model=dict)
    async def mint_soldier(
        soldier_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        """Mint a meme soldier token on the blockchain (placeholder)"""
        # Get the soldier from the database
        soldier = db.query(MemeSoldier).filter(
            MemeSoldier.id == soldier_id,
            MemeSoldier.owner_id == current_user.id
        ).first()
        
        if not soldier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meme soldier not found or you don't have permission"
            )
        
        # Just a placeholder response for now - will implement actual minting later
        return {
            "success": True,
            "message": "Minting functionality will be implemented later",
            "soldier_id": soldier_id,
            "name": soldier.name
        }

@router.get("/test")
async def test_endpoint():
    """Simple test endpoint that doesn't use any external dependencies"""
    return {
        "success": True,
        "message": "Meme generation router is functioning",
        "time": time.time() if 'time' in globals() else None,
        "vercel": IN_VERCEL
    } 