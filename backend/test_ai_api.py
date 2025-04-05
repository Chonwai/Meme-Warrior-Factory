import os
from dotenv import load_dotenv
import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

# Check OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY is not set in the .env file")
    sys.exit(1)

from app.utils.ai import generate_meme_image, generate_meme_soldier_name

# Create meme_images directory if it doesn't exist
os.makedirs("meme_images", exist_ok=True)

app = FastAPI(
    title="MemeWarriors AI Test API",
    description="Test API for MemeWarriors AI functionality",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving images
app.mount("/images", StaticFiles(directory="meme_images"), name="images")

class MemeGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500)

class MemeItem(BaseModel):
    prompt: str
    image_url: str
    coin_icon_url: str
    name: Optional[str] = None

class MemeGenerationResponse(BaseModel):
    success: bool
    items: Optional[List[MemeItem]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "MemeWarriors AI Test API is running",
        "endpoints": {
            "generate_meme": "/generate",
        }
    }

@app.post("/generate", response_model=MemeGenerationResponse)
async def generate_meme(request: MemeGenerationRequest):
    """Generate meme images and names based on a prompt
    
    This endpoint will:
    1. Parse the user prompt to identify 2 distinct items or themes
    2. Generate a pixel art meme image for each item
    3. Generate a name for each meme soldier
    4. Return the results as a list of items
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
            name = generate_meme_soldier_name(item["prompt"])
            
            result_items.append({
                "prompt": item["prompt"],
                "image_url": item["image_url"],
                "coin_icon_url": item["coin_icon_url"],
                "name": name
            })
        
        return {
            "success": True,
            "items": result_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting MemeWarriors AI Test API...")
    uvicorn.run("test_ai_api:app", host="0.0.0.0", port=8000, reload=True) 