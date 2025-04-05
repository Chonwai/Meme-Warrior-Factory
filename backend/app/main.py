from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import importlib
import time
from io import BytesIO
import tempfile
from PIL import Image, ImageDraw, ImageFont

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

@app.get("/api-test")
async def api_test():
    """Extremely basic test endpoint that doesn't rely on any external dependencies"""
    return {
        "success": True,
        "message": "Basic API connectivity test passed",
        "time": time.time(),
        "vercel": IN_VERCEL
    }

@app.get("/safe-openai-test")
async def safe_openai_test():
    """Simple endpoint to test OpenAI integration with better error handling"""
    debug_info = {
        "vercel": IN_VERCEL,
        "steps": []
    }
    
    try:
        # Step 1: Check environment
        debug_info["steps"].append("Checking environment")
        env_vars = {}
        for key in sorted(os.environ.keys()):
            if key.startswith('OPENAI') or key.startswith('VERCEL'):
                # Only show that it exists, not the value
                env_vars[key] = "✓ Set" if os.environ.get(key) else "✗ Not set"
        debug_info["environment_variables"] = env_vars
        
        # Step 2: Try importing OpenAI
        debug_info["steps"].append("Importing OpenAI")
        try:
            from openai import OpenAI
            debug_info["openai_import"] = "Success"
        except Exception as import_error:
            debug_info["openai_import"] = f"Failed: {str(import_error)}"
            return {
                "success": False,
                "message": "Failed to import OpenAI library",
                "debug_info": debug_info
            }
        
        # Step 3: Get API key
        debug_info["steps"].append("Getting API key")
        api_key = None
        try:
            from app.config.settings import settings
            api_key = settings.OPENAI_API_KEY
            debug_info["api_key_source"] = "settings"
        except ImportError:
            api_key = os.environ.get('OPENAI_API_KEY')
            debug_info["api_key_source"] = "environment"
        
        if not api_key:
            debug_info["api_key_found"] = False
            return {
                "success": False,
                "message": "OpenAI API key not found",
                "debug_info": debug_info
            }
        else:
            debug_info["api_key_found"] = True
            # Show partial key for debugging (safely)
            if len(api_key) > 10:
                debug_info["api_key_format"] = f"{api_key[:5]}...{api_key[-4:]}"
        
        # Step 4: Try creating client
        debug_info["steps"].append("Creating OpenAI client")
        try:
            client = OpenAI(api_key=api_key)
            debug_info["client_created"] = True
        except Exception as client_error:
            debug_info["client_error"] = str(client_error)
            return {
                "success": False,
                "message": "Failed to create OpenAI client",
                "debug_info": debug_info
            }
        
        # Step 5: Simple test request (not image generation)
        debug_info["steps"].append("Making simple API request")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a test assistant."},
                    {"role": "user", "content": "Return only the word 'SUCCESS' without quotes or explanation"}
                ],
                max_tokens=10,
                temperature=0
            )
            debug_info["api_request"] = "Success"
            result = response.choices[0].message.content.strip()
            debug_info["api_response"] = result
            
            return {
                "success": True,
                "message": "OpenAI test successful",
                "response": result,
                "debug_info": debug_info
            }
        except Exception as api_error:
            debug_info["api_error"] = str(api_error)
            return {
                "success": False,
                "message": "Failed to make OpenAI API request",
                "debug_info": debug_info
            }
    
    except Exception as e:
        debug_info["error"] = str(e)
        return {
            "success": False,
            "message": "Unexpected error during testing",
            "debug_info": debug_info
        }

@app.get("/test-blob")
async def test_blob():
    """Test endpoint for Vercel Blob storage"""
    try:
        # Check if we're in Vercel
        in_vercel = os.environ.get('VERCEL') == '1'
        if not in_vercel:
            return {
                "success": False,
                "message": "This endpoint is for testing Vercel Blob storage and only works in Vercel."
            }
        
        # Check for Blob token
        blob_token = os.environ.get('BLOB_READ_WRITE_TOKEN')
        if not blob_token:
            return {
                "success": False,
                "message": "BLOB_READ_WRITE_TOKEN environment variable is not set."
            }
        
        # Set environment variable
        os.environ["BLOB_READ_WRITE_TOKEN"] = blob_token
        
        # Create a simple test image
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a test image
        image = Image.new('RGB', (200, 200), color=(73, 109, 137))
        d = ImageDraw.Draw(image)
        d.text((20, 20), "Hello from Vercel Blob!", fill=(255, 255, 0))
        
        # Save to BytesIO
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        img_data = img_io.getvalue()
        
        # Import Vercel Blob SDK
        from vercel_blob import put, PutOptions
        
        # Upload to Vercel Blob
        filename = f"test_blob_{int(time.time())}.png"
        blob = await put(filename, img_data, PutOptions(access="public"))
        
        return {
            "success": True,
            "message": "Successfully uploaded test image to Vercel Blob",
            "url": blob.url,
            "size": blob.size,
            "timestamp": time.time()
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "message": "Failed to test Vercel Blob storage",
            "error": str(e),
            "traceback": traceback.format_exc()
        } 