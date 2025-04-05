import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Blockchain settings - Celo Mainnet (for rewards)
    CELO_MAINNET_RPC_URL: str = os.getenv("CELO_MAINNET_RPC_URL", "https://forno.celo.org")
    REWARD_CONTRACT_ADDRESS: str = os.getenv("REWARD_CONTRACT_ADDRESS", "")
    REWARD_DISTRIBUTOR_ADDRESS: str = os.getenv("REWARD_DISTRIBUTOR_ADDRESS", "")
    
    # Blockchain settings - Testnet (for meme soldiers)
    CELO_TESTNET_RPC_URL: str = os.getenv("CELO_TESTNET_RPC_URL", "https://alfajores-forno.celo-testnet.org")
    SOLDIER_CONTRACT_ADDRESS: str = os.getenv("SOLDIER_CONTRACT_ADDRESS", "")
    
    # Common blockchain settings
    GAS_LIMIT: int = int(os.getenv("GAS_LIMIT", "300000"))
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Redis settings for Celery
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # File storage
    MEME_STORAGE_PATH: str = os.getenv("MEME_STORAGE_PATH", "./meme_images")

settings = Settings() 