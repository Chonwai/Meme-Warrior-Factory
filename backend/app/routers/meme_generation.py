from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.utils.ai import generate_meme_image, generate_meme_soldier_name
from app.utils.auth import get_current_user
from app.models.user import User
from app.models.meme_soldier import MemeSoldier
from app.schemas.meme_soldier import MemeSoldierGeneration, MemeSoldierGenerationResponse

router = APIRouter(
    prefix="/meme",
    tags=["meme generation"],
)

@router.post("/generate", response_model=dict)
async def generate_meme(
    request: MemeSoldierGeneration,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Generate the meme images
        image_result = generate_meme_image(request.prompt)
        
        if not image_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=image_result.get("error", "Failed to generate images")
            )
            
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
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Test endpoint that doesn't save to database
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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=image_result.get("error", "Failed to generate images")
            )
            
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

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