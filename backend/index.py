from fastapi import FastAPI
import os
import sys

# Force Vercel environment variable to be set
os.environ["VERCEL"] = "1"
os.environ["SKIP_FILE_OPERATIONS"] = "1"

# Log environment information
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

try:
    # Import the main FastAPI app
    from app.main import app
    from mangum import Mangum
    
    # Create an API Gateway handler with Mangum
    handler = Mangum(app)
    
    print("Successfully configured FastAPI app with Mangum handler")
    
except Exception as e:
    # If app import fails, create a minimal app
    print(f"Error importing main app: {str(e)}")
    from fastapi import FastAPI
    from mangum import Mangum
    
    minimal_app = FastAPI()
    
    @minimal_app.get("/")
    async def root():
        return {
            "status": "error",
            "message": "Main app failed to load",
            "error": str(e)
        }
    
    # Create handler for minimal app
    handler = Mangum(minimal_app)
 