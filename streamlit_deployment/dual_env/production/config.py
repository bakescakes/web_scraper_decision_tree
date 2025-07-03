"""Production configuration for web scraper system."""

import os
import sys
from typing import Dict, Any

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from constants import PERFORMANCE_TARGETS, BROWSER_SETTINGS, LOGGING, RATE_LIMITING

class ProductionConfig:
    """Production configuration settings optimized for <40s response time."""
    
    # API Configuration (for API server integration)
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "35"))  # Longer timeout for production reliability
    API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "2"))
    
    # Performance settings (optimized for production)
    TIMEOUT_SECONDS = BROWSER_SETTINGS['DEFAULT_TIMEOUT']
    WAIT_TIME_SECONDS = BROWSER_SETTINGS['WAIT_TIME']
    MAX_RETRIES = BROWSER_SETTINGS['MAX_RETRIES']
    
    # Browser settings
    BROWSER_TIMEOUT = 20  # Maximum browser operation time
    LOAD_STRATEGY = BROWSER_SETTINGS['LOAD_STRATEGY']
    USER_AGENT = BROWSER_SETTINGS['USER_AGENT']
    
    # Rate limiting (production optimized)
    REQUEST_DELAY = RATE_LIMITING['REQUEST_DELAY']
    CONCURRENT_LIMIT = RATE_LIMITING['CONCURRENT_LIMIT']
    DOMAIN_COOLDOWN = RATE_LIMITING['DOMAIN_COOLDOWN']
    
    # Logging (production safe)
    LOG_LEVEL = os.getenv('LOG_LEVEL', LOGGING['LEVEL'])
    LOG_FORMAT = LOGGING['FORMAT']
    LOG_DATE_FORMAT = LOGGING['DATE_FORMAT']
    
    # Error handling
    ENABLE_FALLBACKS = True
    MAX_FALLBACK_ATTEMPTS = 2
    
    # Performance targets (critical for production)
    MAX_RESPONSE_TIME = PERFORMANCE_TARGETS['MAX_RESPONSE_TIME']
    TARGET_RESPONSE_TIME = PERFORMANCE_TARGETS['TARGET_RESPONSE_TIME']
    EXCELLENT_RESPONSE_TIME = PERFORMANCE_TARGETS['EXCELLENT_RESPONSE_TIME']
    
    # Quality thresholds
    MIN_SONGS_THRESHOLD = PERFORMANCE_TARGETS['MIN_SONGS_THRESHOLD']
    QUALITY_THRESHOLD = PERFORMANCE_TARGETS['QUALITY_THRESHOLD']
    
    # Environment detection
    IS_PRODUCTION = os.getenv('PRODUCTION', '').lower() in ('true', '1', 'yes')
    IS_STREAMLIT = 'streamlit' in sys.modules or 'STREAMLIT_SHARING' in os.environ
    
    # Streamlit specific settings
    STREAMLIT_CONFIG = {
        'PAGE_TITLE': '🎵 Music List Extractor - Production',
        'PAGE_ICON': '🎵',
        'LAYOUT': 'centered',
        'SIDEBAR_STATE': 'auto'
    }
    
    # Environment
    ENVIRONMENT = "production"
    
    # Feature flags (production optimized)
    SHOW_DEBUG_INFO = os.getenv('SHOW_DEBUG_INFO', 'false').lower() in ('true', '1')
    ENABLE_DEMO_MODE = True
    SHOW_API_STATUS = True
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        return {
            attr: getattr(cls, attr) 
            for attr in dir(cls) 
            if not attr.startswith('_') and not callable(getattr(cls, attr))
        }
    
    @classmethod
    def get_performance_config(cls) -> Dict[str, Any]:
        """Get performance-related configuration."""
        return {
            'max_response_time': cls.MAX_RESPONSE_TIME,
            'target_response_time': cls.TARGET_RESPONSE_TIME,
            'timeout_seconds': cls.TIMEOUT_SECONDS,
            'browser_timeout': cls.BROWSER_TIMEOUT,
            'min_songs_threshold': cls.MIN_SONGS_THRESHOLD,
            'quality_threshold': cls.QUALITY_THRESHOLD
        }
    
    @classmethod
    def get_browser_config(cls) -> Dict[str, Any]:
        """Get browser-related configuration."""
        return {
            'timeout': cls.BROWSER_TIMEOUT,
            'load_strategy': cls.LOAD_STRATEGY,
            'user_agent': cls.USER_AGENT,
            'wait_time': cls.WAIT_TIME_SECONDS,
            'max_retries': cls.MAX_RETRIES
        }
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API-related configuration."""
        return {
            'api_base_url': cls.API_BASE_URL,
            'api_timeout': cls.API_TIMEOUT,
            'api_max_retries': cls.API_MAX_RETRIES,
            'environment': cls.ENVIRONMENT,
            'show_debug_info': cls.SHOW_DEBUG_INFO,
            'enable_demo_mode': cls.ENABLE_DEMO_MODE,
            'show_api_status': cls.SHOW_API_STATUS
        }
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """Get all configuration settings including API config."""
        base_config = cls.get_config()
        api_config = cls.get_api_config()
        return {**base_config, **api_config}