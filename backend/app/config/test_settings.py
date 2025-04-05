import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # File storage
    MEME_STORAGE_PATH: str = os.getenv("MEME_STORAGE_PATH", "./meme_images")

settings = Settings() 