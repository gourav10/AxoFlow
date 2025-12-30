from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "AxoFlow API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Job Copilot - Automated Job Application System"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend port
        "http://localhost:8000",  # Backend itself
    ]
    
    # Security (placeholder values)
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database (placeholder)
    DATABASE_URL: str = "sqlite:///./axoflow.db"
    
    # NocoDB Configuration
    NOCODB_URL: str = "https://anton-server-station.tailfa58fb.ts.net:8081"
    NOCODB_API_TOKEN: str = ""  # Set via environment variable
    NOCODB_BASE_ID: str = ""    # Set via environment variable
    NOCODB_TABLE_ID: str = ""   # Set via environment variable (Candidates table)
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
