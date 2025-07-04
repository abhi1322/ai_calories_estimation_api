from pydantic import BaseSettings
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings(BaseSettings):
    openrouter_api_key: str
    vision_model: str
    structuring_model: str
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
