from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routers import auth, meme_generation, battles, assets, users
from app.config.settings import settings

# Create meme_images directory if it doesn't exist
os.makedirs(settings.MEME_STORAGE_PATH, exist_ok=True)

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

# Mount static files for serving images
app.mount("/images", StaticFiles(directory=settings.MEME_STORAGE_PATH), name="images")

# Include routers
app.include_router(auth.router)
app.include_router(meme_generation.router)
app.include_router(battles.router)
app.include_router(assets.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to MemeWarriors API",
        "docs": "/docs"
    } 