#!/usr/bin/env python3
"""
Railway Entry Point - Redirects to v3.0.0 Production API
This file ensures Railway deploys our v3.0.0 Playwright extraction code
"""

import sys
import os
from pathlib import Path

# Add the correct path for our production API
sys.path.insert(0, str(Path(__file__).parent / "mcp_api_server" / "production"))

# Import and run the production API
try:
    from mcp_api_server.production.main import app
    print("✅ Successfully loaded v3.0.0 Production API")
    print("🎵 Real Playwright song extraction enabled")
except ImportError as e:
    print(f"❌ Failed to load production API: {e}")
    # Fallback - but this shouldn't happen
    from fastapi import FastAPI
    app = FastAPI(title="Import Error", description=f"Failed to load: {e}")

# This is what Railway will import when it runs "uvicorn main:app"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))