from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Trip Tales API"
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/trip_tales_db"
    
    # Security
    SECRET_KEY: str = "trip-tales-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "video/mp4", "video/avi", "video/mov"]
    UPLOAD_DIR: str = "uploads"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # AI Service (placeholder for future integration)
    AI_SERVICE_URL: Optional[str] = None
    AI_SERVICE_API_KEY: Optional[str] = None
    
    # Video Processing Settings
    VIDEO_FPS: int = 30  # Frames per second
    VIDEO_RESOLUTION: tuple = (1920, 1080)  # Full HD
    VIDEO_CODEC: str = "mp4v"  # or "avc1" for H.264
    PHOTO_DURATION: int = 1  # Duration per photo in seconds
    TRANSITION_FRAMES: int = 15  # Frames for fade transitions (0.5s at 30fps)
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)