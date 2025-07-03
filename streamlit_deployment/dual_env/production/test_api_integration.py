"""
Test production API integration
Validates that the production app can connect to and use the API server
"""

import sys
import os
from typing import Dict, Any

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from api_client import APIClient, APIConnectionError, APIExtractionError, check_api_health
from config import ProductionConfig

def test_api_health():
    """Test API server health check."""
    print("🔍 Testing API health...")
    
    try:
        health = check_api_health(ProductionConfig.API_BASE_URL)
        print(f"✅ API Health Check: {health}")
        return True
    except Exception as e:
        print(f"❌ API Health Check Failed: {e}")
        return False

def test_api_connection():
    """Test API client connection."""
    print("🔍 Testing API connection...")
    
    try:
        client = APIClient(ProductionConfig.API_BASE_URL, ProductionConfig.API_TIMEOUT)
        connected = client.test_connection()
        
        if connected:
            print("✅ API Connection: Successful")
            return True
        else:
            print("❌ API Connection: Failed")
            return False
    except Exception as e:
        print(f"❌ API Connection Exception: {e}")
        return False

def test_api_extraction():
    """Test API song extraction with a simple URL."""
    print("🔍 Testing API extraction...")
    
    try:
        client = APIClient(ProductionConfig.API_BASE_URL, ProductionConfig.API_TIMEOUT)
        
        # Use a simple URL that should work with HTTP fallback
        test_url = "https://pitchfork.com/features/lists-and-guides/best-songs-2024/"
        
        result = client.extract_songs(test_url)
        songs = result.get('songs', [])
        
        print(f"✅ API Extraction: {len(songs)} songs extracted")
        if songs:
            print(f"   Sample songs: {songs[:3]}")
        
        return len(songs) > 0
        
    except APIConnectionError as e:
        print(f"❌ API Connection Error: {e}")
        return False
    except APIExtractionError as e:
        print(f"❌ API Extraction Error: {e}")
        return False
    except Exception as e:
        print(f"❌ API Extraction Exception: {e}")
        return False

def test_production_config():
    """Test production configuration."""
    print("🔍 Testing production configuration...")
    
    config = ProductionConfig.get_api_config()
    
    # Validate essential config
    checks = [
        (config['api_base_url'].startswith('http'), "API base URL format"),
        (config['api_timeout'] >= 10, "API timeout value"),
        (config['environment'] == 'production', "Environment setting"),
        (isinstance(config['show_debug_info'], bool), "Debug info setting")
    ]
    
    all_passed = True
    for check, description in checks:
        if check:
            print(f"✅ {description}: OK")
        else:
            print(f"❌ {description}: Failed")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests."""
    print("🚀 Production API Integration Testing")
    print("=" * 50)
    
    tests = [
        ("API Health Check", test_api_health),
        ("Production Config", test_production_config),
        ("API Connection", test_api_connection),
        ("API Extraction", test_api_extraction)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        results[test_name] = test_func()
    
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Production API integration ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())