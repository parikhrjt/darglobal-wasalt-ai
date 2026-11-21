"""
Application Configuration
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DarGlobal & Wasalt AI Agentic Real Estate Copilot"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))

    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv(
        "OPENROUTER_MODEL", 
        "meta-llama/llama-3.3-70b-instruct:free"
    )
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    SITE_URL: str = os.getenv("SITE_URL", "https://darglobal-ai.internal")
    SITE_NAME: str = "DarGlobal AI Assistant"

    # Supported OpenRouter Free Models
    FREE_MODELS: List[str] = [
        "meta-llama/llama-3.3-70b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen-2.5-72b-instruct:free",
        "deepseek/deepseek-r1:free",
        "google/gemini-2.0-flash-exp:free"
    ]

    # Data file paths
    CONSOLIDATED_DATA_PATH: str = os.getenv("CONSOLIDATED_DATA_PATH", "data/consolidated_properties.json")
    DARGLOBAL_DATA_PATH: str = os.getenv("DARGLOBAL_DATA_PATH", "data/darglobal_projects.json")
    WASALT_DATA_PATH: str = os.getenv("WASALT_DATA_PATH", "data/wasalt_properties.json")
    LEADS_DATA_PATH: str = os.getenv("LEADS_DATA_PATH", "data/leads.json")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
