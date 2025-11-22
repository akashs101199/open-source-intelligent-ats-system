"""
Configuration management for the ATS system
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Intelligent ATS for Agentic AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Ollama LLM
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b"
    OLLAMA_TIMEOUT: Optional[int] = None  # No timeout - let it run as long as needed
    
    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # Qdrant Vector DB
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "candidates"
    
    # Scoring Weights (for Agentic AI roles)
    WEIGHT_AGENTIC: float = 0.35
    WEIGHT_TECHNICAL: float = 0.30
    WEIGHT_SEMANTIC: float = 0.20
    WEIGHT_EXPERIENCE: float = 0.15
    
    # Processing
    MAX_RESUME_SIZE_MB: int = 10
    MAX_CANDIDATES_PER_MATCH: int = 20
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()