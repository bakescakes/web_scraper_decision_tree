#!/usr/bin/env python3
"""
Railway Entry Point - v3.0.0 Production API with Real Playwright Extraction
This loads our proven Playwright production extractor that we built together
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime

# Add paths for our existing extractors
sys.path.insert(0, str(Path(__file__).parent))

# Import our existing robust extraction code
try:
    from extractors.playwright_production_extractor import extract_songs_production_async
    print("✅ Loaded existing Playwright production extractor")
    PLAYWRIGHT_EXTRACTOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Playwright extractor not available: {e}")
    try:
        # Fallback to railway_deployment location
        from railway_deployment.extractors.playwright_production_extractor import extract_songs_production_async
        print("✅ Loaded Playwright extractor from railway_deployment")
        PLAYWRIGHT_EXTRACTOR_AVAILABLE = True
    except ImportError:
        PLAYWRIGHT_EXTRACTOR_AVAILABLE = False

try:
    from comprehensive_song_extractor import ComprehensiveSongExtractor
    print("✅ Loaded comprehensive song extractor")
    COMPREHENSIVE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Comprehensive extractor not available: {e}")
    COMPREHENSIVE_AVAILABLE = False

try:
    from extractors.lightweight_extractor import extract_songs_lightweight_async
    print("✅ Loaded lightweight requests extractor")
    LIGHTWEIGHT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Lightweight extractor not available: {e}")
    LIGHTWEIGHT_AVAILABLE = False

# Create FastAPI app with our proven extraction logic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Web Scraper API v3.0.0 - Real Playwright Extraction",
    description="Production API using our proven Playwright extraction logic",
    version="3.0.0-playwright-production"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "3.0.0-playwright-production",
        "timestamp": datetime.now().isoformat(),
        "playwright_available": PLAYWRIGHT_EXTRACTOR_AVAILABLE,
        "comprehensive_available": COMPREHENSIVE_AVAILABLE,
        "lightweight_available": LIGHTWEIGHT_AVAILABLE
    }

@app.get("/extract")
async def extract_songs(url: str, max_songs: int = 10):
    """Real song extraction using our proven Playwright logic"""
    print(f"🎵 Extracting songs from: {url}")
    
    try:
        if PLAYWRIGHT_EXTRACTOR_AVAILABLE:
            print("🎭 Using Playwright production extractor...")
            result = await extract_songs_production_async(url, expected_count=max_songs)
            
            return {
                "success": result.get("success", True),
                "url": url,
                "songs_found": result.get("actual_count", len(result.get("songs", []))),
                "songs": result.get("songs", [])[:max_songs],
                "method": result.get("method", "playwright_direct"),
                "version": "3.0.0-playwright-production",
                "execution_time": result.get("execution_time", 0),
                "timestamp": datetime.now().isoformat()
            }
            
        elif LIGHTWEIGHT_AVAILABLE:
            print("🚀 Using lightweight requests extractor...")
            result = await extract_songs_lightweight_async(url, expected_count=max_songs)
            
            return {
                "success": result.get("success", True),
                "url": url,
                "songs_found": result.get("actual_count", len(result.get("songs", []))),
                "songs": result.get("songs", [])[:max_songs],
                "method": result.get("method", "lightweight_requests"),
                "version": "3.0.0-lightweight",
                "execution_time": result.get("execution_time", 0),
                "timestamp": datetime.now().isoformat()
            }
            
        elif COMPREHENSIVE_AVAILABLE:
            print("🔧 Using comprehensive extractor...")
            extractor = ComprehensiveSongExtractor()
            result = extractor.extract_songs_comprehensive(url, expected_count=max_songs)
            
            return {
                "success": True,
                "url": url,
                "songs_found": len(result.get("songs", [])),
                "songs": result.get("songs", [])[:max_songs],
                "method": "comprehensive_extractor",
                "version": "3.0.0-comprehensive",
                "timestamp": datetime.now().isoformat()
            }
            
        else:
            # This should not happen with our existing codebase
            raise HTTPException(status_code=500, detail="No extraction methods available")
            
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

print("🚀 v3.0.0 API with proven Playwright extraction ready!")

# This is what Railway will import when it runs "uvicorn main:app"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))