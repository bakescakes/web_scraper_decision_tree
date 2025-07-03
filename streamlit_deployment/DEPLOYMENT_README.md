# Web Scraper Decision Tree - Streamlit Deployment

## Quick Start

This is a cloud-native song extraction system with API-first architecture.

### Files Included
- `streamlit_app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `dual_env/` - Production code and configuration
- `.streamlit/` - Streamlit configuration

### Deployment
1. Deploy to Streamlit Cloud
2. Set main file: `streamlit_app.py`
3. Configure secrets in Streamlit Cloud dashboard

### Configuration
Add these secrets in Streamlit Cloud:
```
API_BASE_URL = "https://your-api-server.railway.app"
API_TIMEOUT = "35"
ENVIRONMENT = "production"
```

### Support
For issues, check the original repository documentation.
