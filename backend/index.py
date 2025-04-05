import os
import time
import sys

# Force Vercel environment variable to be set before any imports
os.environ["VERCEL"] = "1"
os.environ["SKIP_FILE_OPERATIONS"] = "1"

# Log the current environment
print("Current environment:")
print(f"- Python version: {sys.version}")
print(f"- Working directory: {os.getcwd()}")
print(f"- Environment variables: {[k for k in os.environ.keys() if k.startswith('PYTHON') or k == 'VERCEL' or k == 'SKIP_FILE_OPERATIONS']}")

try:
    # Try to import the main app with a simpler approach
    print("Attempting to import FastAPI app...")
    from fastapi import FastAPI
    from app.main import app as main_app
    print("Successfully imported app.main")
    
    # Create handler for Vercel
    handler = main_app
    
except Exception as e:
    # If importing fails, create a minimal app
    print(f"Error importing app.main: {str(e)}")
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {
            "success": False,
            "message": "Minimal fallback app - main app failed to load",
            "error": str(e),
            "vercel": os.environ.get('VERCEL') == '1',
            "timestamp": time.time()
        }
    
    @app.get("/debug")
    async def debug():
        return {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "directory_contents": os.listdir(),
            "environment": {k: v for k, v in os.environ.items() 
                          if k.startswith('PYTHON') or k == 'VERCEL' or k == 'SKIP_FILE_OPERATIONS'}
        }
    
    # Create handler for Vercel
    handler = app
 