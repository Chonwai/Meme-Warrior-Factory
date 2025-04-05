import os
from app.main import app

# Import FastAPI with a simple app variable at the top level for Vercel
# No need for Mangum when using Vercel's FastAPI support

if __name__ == "__main__":
    # For local development only
    import uvicorn
    from app.config.settings import settings
    
    # Create meme_images directory if it doesn't exist
    os.makedirs(settings.MEME_STORAGE_PATH, exist_ok=True)
    
    # Start the server
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        log_level="info"
    )
