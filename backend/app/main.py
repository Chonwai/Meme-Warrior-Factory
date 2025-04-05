from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import importlib

# Detect if we're running in Vercel
IN_VERCEL = os.environ.get('VERCEL') == '1'

app = FastAPI(
    title="MemeWarriors API",
    description="API for MemeWarriors - Generate and battle with meme soldiers on Celo blockchain",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create meme_images directory if it doesn't exist
os.makedirs(os.environ.get('MEME_STORAGE_PATH', './meme_images'), exist_ok=True)

# Mount static files for serving images - only if not in Vercel
if not IN_VERCEL:
    app.mount("/images", StaticFiles(directory=os.environ.get('MEME_STORAGE_PATH', './meme_images')), name="images")

# Import and include routers, with fallbacks for missing dependencies in Vercel
try:
    from app.routers import meme_generation
    app.include_router(meme_generation.router)
except ImportError as e:
    print(f"Error importing meme_generation router: {e}")

# Only include these routers if not in Vercel, as they depend on web3/aiohttp
if not IN_VERCEL:
    try:
        from app.routers import auth, battles, assets, users
        app.include_router(auth.router)
        app.include_router(battles.router)
        app.include_router(assets.router)
        app.include_router(users.router)
    except ImportError as e:
        print(f"Error importing non-essential routers: {e}")

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to MemeWarriors API",
        "docs": "/docs",
        "environment": "Vercel" if IN_VERCEL else "Development"
    }

@app.get("/test-openai")
async def test_openai():
    """Simple endpoint to test OpenAI integration"""
    try:
        from openai import OpenAI
        
        # Get API key with fallback
        api_key = None
        try:
            from app.config.settings import settings
            api_key = settings.OPENAI_API_KEY
        except ImportError:
            api_key = os.environ.get('OPENAI_API_KEY')
        
        if not api_key:
            return {
                "success": False,
                "error": "OpenAI API key not found"
            }
        
        # Test OpenAI connection
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=10
        )
        
        return {
            "success": True,
            "message": response.choices[0].message.content,
            "model": response.model
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        } 