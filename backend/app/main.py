from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import time
import importlib

# Detect if we're running in Vercel
IN_VERCEL = os.environ.get('VERCEL') == '1'
SKIP_FILE_OPERATIONS = os.environ.get('SKIP_FILE_OPERATIONS') == '1'

# Print some debug info
print(f"Starting FastAPI app in {'Vercel' if IN_VERCEL else 'local'} environment")
print(f"SKIP_FILE_OPERATIONS: {SKIP_FILE_OPERATIONS}")
print(f"Working directory: {os.getcwd()}")

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

# Only create directories and mount static files in local environment
if not IN_VERCEL and not SKIP_FILE_OPERATIONS:
    from fastapi.staticfiles import StaticFiles
    try:
        meme_storage_path = os.environ.get('MEME_STORAGE_PATH', './meme_images')
        os.makedirs(meme_storage_path, exist_ok=True)
        app.mount("/images", StaticFiles(directory=meme_storage_path), name="images")
        print(f"Mounted static files from {meme_storage_path}")
    except Exception as e:
        print(f"Warning: Could not set up static files: {str(e)}")

# Import and include routers
try:
    from app.routers import meme_generation
    app.include_router(meme_generation.router)
    print("Successfully imported and included meme_generation router")
except Exception as e:
    print(f"Error importing meme_generation router: {e}")

# Only include these routers if not in Vercel, as they depend on web3/aiohttp
if not IN_VERCEL:
    try:
        from app.routers import auth, battles, assets, users
        app.include_router(auth.router)
        app.include_router(battles.router)
        app.include_router(assets.router)
        app.include_router(users.router)
        print("Successfully imported and included additional routers")
    except Exception as e:
        print(f"Error importing non-essential routers: {e}")

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to MemeWarriors API",
        "docs": "/docs",
        "environment": "Vercel" if IN_VERCEL else "Development"
    }

@app.get("/minimal-test")
async def minimal_test():
    """The most basic test endpoint that doesn't use any filesystem operations or external dependencies"""
    return {
        "success": True,
        "message": "API is functioning correctly",
        "environment": "Vercel" if IN_VERCEL else "Local",
        "timestamp": time.time()
    }

@app.get("/env-info")
async def env_info():
    """Simple endpoint to show environment information without any external dependencies"""
    import platform
    
    # Collect information without revealing sensitive data
    env_vars = {}
    for key in os.environ:
        # Only show if environment variables exist, not their values
        if key.startswith('OPEN') or key.startswith('MEME') or key == 'VERCEL' or key.startswith('BLOB') or key.startswith('PYTHON'):
            env_vars[key] = "Set" if os.environ.get(key) else "Not set"
    
    try:
        directory_contents = os.listdir() 
    except:
        directory_contents = ["Could not list directory"]
    
    return {
        "success": True,
        "python_version": sys.version,
        "platform": platform.platform(),
        "environment": "Vercel" if os.environ.get('VERCEL') == '1' else "Local",
        "environment_variables": env_vars,
        "current_directory": os.getcwd(),
        "directory_contents": directory_contents,
        "timestamp": time.time()
    } 