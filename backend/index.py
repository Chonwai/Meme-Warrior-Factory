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
    from app.main import app
    
    # Define handler function - use the app directly instead of wrapping it
    handler = app
    
    print("Successfully imported app.main and created handler")
    
except Exception as e:
    # If importing fails, create a minimal app
    print(f"Error importing app.main: {str(e)}")
    from fastapi import FastAPI
    
    minimal_app = FastAPI()
    
    @minimal_app.get("/")
    async def root():
        return {
            "success": False,
            "message": "Minimal fallback app - main app failed to load",
            "error": str(e),
            "vercel": os.environ.get('VERCEL') == '1',
            "timestamp": time.time()
        }
    
    @minimal_app.get("/debug")
    async def debug():
        return {
            "python_version": sys.version,
            "working_directory": os.getcwd(),
            "directory_contents": os.listdir(),
            "environment": {k: v for k, v in os.environ.items() 
                          if k.startswith('PYTHON') or k == 'VERCEL' or k == 'SKIP_FILE_OPERATIONS'}
        }
    
    # Use the minimal app directly as the handler
    handler = minimal_app
 