from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "InteliDoc"
    
    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://intelidoc.netlify.app",
        "https://*.netlify.app"  # Allow all Netlify subdomains
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/intelidoc"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Google Gemini
    GEMINI_API_KEY: str = "AIzaSyDXwKY9Xf_iNHsPV6L7NGnf95qOZDkvOy0"  # Hardcoded for testing
    GEMINI_MODEL: str = "models/gemini-2.5-flash-live-preview"
    GEMINI_MAX_TOKENS: int = 4000
    GEMINI_TEMPERATURE: float = 0.1
    
    # Pinecone
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    PINECONE_INDEX_NAME: str = "intelidoc-embeddings"
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = ""
    AWS_REGION: str = "us-east-1"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".txt"]
    
    # AI Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_CHUNKS_PER_DOCUMENT: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        # Don't override hardcoded API key with .env
        env_ignore = ["GEMINI_API_KEY"]

# Create settings instance
settings = Settings() 