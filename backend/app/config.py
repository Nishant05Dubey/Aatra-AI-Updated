from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://aatra_user:aatra_pass@localhost:5432/aatra_db"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Twitter API
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    twitter_access_token: Optional[str] = None
    twitter_access_token_secret: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    
    # Gemini AI API
    gemini_api_key: Optional[str] = None
    
    # Security
    secret_key: str = "your-super-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App settings
    environment: str = "development"
    api_v1_str: str = "/api/v1"
    project_name: str = "Aatra AI - Anti-India Hate Detection System"
    
    # ML Model settings
    model_name: str = "unitary/toxic-bert"
    confidence_threshold: float = 0.7
    
    # Monitoring keywords for social media
    monitoring_keywords: list = [
        "anti india", "hate india", "destroy india", "india terrorist", 
        "fake india", "india fake", "pakistan zindabad against india",
        "india down", "boycott india", "india enemy"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()