"""
Production configuration for MCP API Server
"""

import os
from typing import Optional


class ProductionConfig:
    """Production environment configuration"""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    
    # Environment
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    
    # API settings
    API_PREFIX: str = "/api/v1"
    TITLE: str = "MCP API Server v3.0.0 - Real Playwright Extraction"
    DESCRIPTION: str = "Song extraction API using MCP browser automation with real Playwright extraction"
    VERSION: str = "3.0.0-playwright-production"
    
    # MCP settings
    MCP_TIMEOUT: int = 40
    MCP_MAX_RETRIES: int = 3
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS settings (restrictive for production)
    CORS_ORIGINS: list = [
        "https://your-streamlit-app.streamlit.app",
        "https://your-domain.com"
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["GET", "POST"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 30
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Security
    API_KEY_HEADER: str = "X-API-Key"
    REQUIRE_API_KEY: bool = False  # Will be enabled in Phase 3.3
    
    @classmethod
    def from_env(cls) -> "ProductionConfig":
        """Load configuration from environment variables"""
        config = cls()
        
        # Override with environment variables if present
        config.HOST = os.getenv("HOST", config.HOST)
        config.PORT = int(os.getenv("PORT", config.PORT))
        config.MCP_TIMEOUT = int(os.getenv("MCP_TIMEOUT", config.MCP_TIMEOUT))
        config.MCP_MAX_RETRIES = int(os.getenv("MCP_MAX_RETRIES", config.MCP_MAX_RETRIES))
        config.REQUIRE_API_KEY = os.getenv("REQUIRE_API_KEY", "false").lower() == "true"
        
        # CORS origins from environment
        cors_origins = os.getenv("CORS_ORIGINS")
        if cors_origins:
            config.CORS_ORIGINS = cors_origins.split(",")
        
        return config


# Global configuration instance
config = ProductionConfig.from_env()