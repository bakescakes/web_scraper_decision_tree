"""Shared constants for both production and development environments."""

# Performance constants
PERFORMANCE_TARGETS = {
    'MAX_RESPONSE_TIME': 40,  # Maximum acceptable response time in seconds
    'TARGET_RESPONSE_TIME': 15,  # Target response time in seconds
    'EXCELLENT_RESPONSE_TIME': 5,  # Excellent response time in seconds
    'MIN_SONGS_THRESHOLD': 5,  # Minimum songs for successful extraction
    'QUALITY_THRESHOLD': 0.7,  # Minimum quality score for valid extraction
}

# Browser automation constants
BROWSER_SETTINGS = {
    'DEFAULT_TIMEOUT': 15,  # Default timeout in seconds
    'WAIT_TIME': 1,  # Default wait time in seconds
    'MAX_RETRIES': 2,  # Maximum retry attempts
    'LOAD_STRATEGY': 'domcontentloaded',  # Browser load strategy
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Site classification constants
SITE_TYPES = {
    'CHART': 'chart',
    'EDITORIAL': 'editorial',
    'LYRICS': 'lyrics',
    'STREAMING': 'streaming',
    'GENERIC': 'generic'
}

# Supported music sites
MUSIC_SITES = {
    'pitchfork.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'medium',
        'requires_browser': True
    },
    'rollingstone.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'medium',
        'requires_browser': True
    },
    'billboard.com': {
        'type': SITE_TYPES['CHART'],
        'complexity': 'high',
        'requires_browser': True
    },
    'genius.com': {
        'type': SITE_TYPES['LYRICS'],
        'complexity': 'medium',
        'requires_browser': True
    },
    'npr.org': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'low',
        'requires_browser': False
    },
    'complex.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'high',
        'requires_browser': True
    },
    'guardian.co.uk': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'low',
        'requires_browser': False
    },
    'stereogum.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'medium',
        'requires_browser': True
    },
    'pastemagazine.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'medium',
        'requires_browser': True
    },
    'spin.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'low',
        'requires_browser': False
    },
    'allmusic.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'medium',
        'requires_browser': True
    },
    'metacritic.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'medium',
        'requires_browser': True
    },
    'nme.com': {
        'type': SITE_TYPES['EDITORIAL'],
        'complexity': 'medium',
        'requires_browser': True
    }
}

# Extraction patterns
PATTERN_TYPES = {
    'NUMBERED_DASH': 'numbered_dash',
    'QUOTED_TITLE': 'quoted_title',
    'ARTIST_SONG': 'artist_song',
    'SONG_BY_ARTIST': 'song_by_artist',
    'GENERIC_DASH': 'generic_dash',
    'CHART_POSITION': 'chart_position',
    'HIP_HOP_FORMAT': 'hip_hop_format'
}

# Quality metrics
QUALITY_METRICS = {
    'FORMAT_WEIGHT': 0.4,  # Weight for proper formatting
    'DUPLICATE_WEIGHT': 0.3,  # Weight for duplicate detection
    'LENGTH_WEIGHT': 0.2,  # Weight for reasonable length
    'CONTENT_WEIGHT': 0.1,  # Weight for content quality
    'MIN_SONG_LENGTH': 5,  # Minimum song string length
    'MAX_SONG_LENGTH': 200,  # Maximum song string length
    'IDEAL_SONG_LENGTH': 50  # Ideal song string length
}

# Rate limiting constants
RATE_LIMITING = {
    'REQUEST_DELAY': 0.5,  # Delay between requests in seconds
    'CONCURRENT_LIMIT': 3,  # Maximum concurrent requests
    'DOMAIN_COOLDOWN': 2,  # Cooldown per domain in seconds
    'RETRY_BACKOFF': 1.5,  # Backoff multiplier for retries
}

# Logging constants
LOGGING = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'DATE_FORMAT': '%Y-%m-%d %H:%M:%S',
    'MAX_LOG_SIZE': 10 * 1024 * 1024,  # 10MB
    'BACKUP_COUNT': 5
}

# Environment detection constants
ENVIRONMENT_INDICATORS = {
    'PRODUCTION_ENV_VARS': ['PRODUCTION', 'PROD', 'STREAMLIT_SHARING'],
    'DEVELOPMENT_ENV_VARS': ['DEVELOPMENT', 'DEV', 'DEBUG'],
    'TESTING_ENV_VARS': ['TESTING', 'TEST', 'PYTEST']
}

# Error handling constants
ERROR_HANDLING = {
    'MAX_FALLBACK_ATTEMPTS': 2,
    'TIMEOUT_ERRORS': ['timeout', 'timed out', 'connection timeout'],
    'BLOCKED_ERRORS': ['403', '429', 'blocked', 'rate limited'],
    'NETWORK_ERRORS': ['network', 'connection', 'dns', 'resolve'],
    'CONTENT_ERRORS': ['no content', 'empty response', 'invalid html']
}

# Validation constants
VALIDATION = {
    'MIN_SONGS_SUCCESS': 1,  # Minimum songs for successful extraction
    'MIN_SONGS_GOOD': 10,  # Minimum songs for good extraction
    'MIN_SONGS_EXCELLENT': 25,  # Minimum songs for excellent extraction
    'MAX_DUPLICATE_RATIO': 0.1,  # Maximum acceptable duplicate ratio
    'MIN_FORMAT_RATIO': 0.7,  # Minimum acceptable format ratio
    'MIN_QUALITY_SCORE': 0.5  # Minimum acceptable quality score
}

# File paths and naming
FILE_PATHS = {
    'RESULTS_DIR': 'results',
    'LOGS_DIR': 'logs',
    'CACHE_DIR': 'cache',
    'TEMP_DIR': 'temp',
    'BACKUP_DIR': 'backups'
}

# API endpoints and services
API_ENDPOINTS = {
    'HEALTH_CHECK': '/health',
    'EXTRACT_SONGS': '/extract',
    'BATCH_EXTRACT': '/batch',
    'VALIDATE_URL': '/validate',
    'METRICS': '/metrics'
}

# Feature flags
FEATURE_FLAGS = {
    'ENABLE_CACHING': True,
    'ENABLE_PERFORMANCE_MONITORING': True,
    'ENABLE_RATE_LIMITING': True,
    'ENABLE_FALLBACK_STRATEGIES': True,
    'ENABLE_BATCH_PROCESSING': True,
    'ENABLE_EXPERIMENTAL_FEATURES': False
}

# Version information
VERSION_INFO = {
    'VERSION': '1.0.0',
    'BUILD_DATE': '2025-01-02',
    'ENVIRONMENT': 'dual_env',
    'AUTHOR': 'Memex AI Assistant',
    'DESCRIPTION': 'Production-ready web scraper with dual environment architecture'
}