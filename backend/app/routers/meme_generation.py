from fastapi import APIRouter, Query
from typing import Optional
import os
import time

# Define a router with tags
router = APIRouter(
    prefix="/meme",
    tags=["meme generation"],
)

# Detect if we're running in Vercel
IN_VERCEL = os.environ.get('VERCEL') == '1'

# Only import dependencies if not in Vercel environment
if not IN_VERCEL:
    # These imports might fail in Vercel, but that's ok as they're not used there
    try:
        from fastapi import Depends, HTTPException, status
        from sqlalchemy.orm import Session
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

@router.post("/generate", response_model=None)
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
            image_result = await generate_meme_image(request.prompt)
            
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
        image_result = await generate_meme_image(request.prompt)
        
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

@router.post("/generate_test", response_model=None)
async def generate_meme_test(
    request: MemeSoldierGeneration
):
    """Test endpoint to generate meme images without authentication or database storage
    
    This endpoint is intended for frontend testing only.
    """
    debug_info = {
        "vercel": os.environ.get('VERCEL') == '1',
        "current_directory": os.getcwd(),
        "environment_vars": [k for k in os.environ.keys() if k.startswith('OPEN') or k.startswith('MEME') or k.startswith('BLOB') or k == 'VERCEL']
    }
    
    try:
        # Generate the meme images
        print(f"Processing prompt: {request.prompt}")
        debug_info["prompt"] = request.prompt
        debug_info["generating_images"] = "attempting"
        
        # Generate images (this is now async)
        image_result = await generate_meme_image(request.prompt)
        debug_info["generating_images"] = "completed"
        debug_info["image_result_success"] = image_result["success"]
        
        if not image_result["success"]:
            error_detail = image_result.get("error", "Failed to generate images")
            debug_info["error_detail"] = error_detail
            return {
                "success": False,
                "error": error_detail,
                "debug_info": debug_info
            }
            
        # Generate names for each item
        debug_info["generated_item_count"] = len(image_result["items"])
        result_items = []
        
        for idx, item in enumerate(image_result["items"]):
            try:
                # Generate a name for this meme soldier
                debug_info[f"item_{idx}_prompt"] = item["prompt"]
                name = generate_meme_soldier_name(item["prompt"])
                debug_info[f"item_{idx}_name"] = name
                
                result_items.append({
                    "id": 999,  # Dummy ID
                    "name": name,
                    "prompt": item["prompt"],
                    "image_url": item["image_url"],
                    "coin_icon_url": item["coin_icon_url"]
                })
            except Exception as item_error:
                debug_info[f"item_{idx}_error"] = str(item_error)
                # Continue with next item
        
        return {
            "success": True,
            "items": result_items,
            "debug_info": debug_info
        }
    except Exception as e:
        debug_info["error"] = str(e)
        debug_info["error_type"] = type(e).__name__
        import traceback
        debug_info["traceback"] = traceback.format_exc()
        
        return {
            "success": False,
            "error": str(e),
            "debug_info": debug_info
        }

# Only include this endpoint if not in Vercel
if not IN_VERCEL:
    @router.post("/mint/{soldier_id}", response_model=None)
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
            # Return error response instead of raising an exception
            return {
                "success": False,
                "error": "Meme soldier not found or you don't have permission"
            }
        
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