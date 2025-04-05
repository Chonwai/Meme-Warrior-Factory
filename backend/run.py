import os
import uvicorn
from app.config.settings import settings

# from init_db import init_db, create_test_data

if __name__ == "__main__":
    # Create meme_images directory if it doesn't exist
    # os.makedirs(settings.MEME_STORAGE_PATH, exist_ok=True)

    # Initialize the database if needed
    # init_db()

    # Create test data
    # create_test_data()

    # Start the server
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
