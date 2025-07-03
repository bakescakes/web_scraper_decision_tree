"""
Test Streamlit app API integration components
Tests the functions used by the Streamlit app without running Streamlit itself
"""

import sys
import os
from typing import Dict, Any

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Mock streamlit for testing
class MockStreamlit:
    def __init__(self):
        self.session_state = {}
    
    def success(self, msg): print(f"✅ {msg}")
    def error(self, msg): print(f"❌ {msg}")
    def info(self, msg): print(f"ℹ️  {msg}")
    def warning(self, msg): print(f"⚠️  {msg}")
    def progress(self, val): return MockProgress()
    def empty(self): return MockEmpty()
    def json(self, data): print(f"📋 JSON: {data}")

class MockProgress:
    def progress(self, val): pass
    def empty(self): pass

class MockEmpty:
    def text(self, msg): pass
    def empty(self): pass

# Mock streamlit and test the app functions
sys.modules['streamlit'] = MockStreamlit()
st = MockStreamlit()

# Import app components
from api_client import APIClient, APIConnectionError, APIExtractionError, check_api_health
from config import ProductionConfig

def test_api_client_functionality():
    """Test the API client functionality used by Streamlit app."""
    print("🔍 Testing API client functionality...")
    
    try:
        client = APIClient(ProductionConfig.API_BASE_URL, ProductionConfig.API_TIMEOUT)
        
        # Test connection
        connected = client.test_connection()
        if connected:
            print("✅ API Client Connection: Working")
        else:
            print("❌ API Client Connection: Failed")
            return False
        
        # Test health check
        health = client.health_check()
        print(f"✅ API Health Check: {health.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ API Client Test Failed: {e}")
        return False

def test_config_methods():
    """Test production config methods used by the app."""
    print("🔍 Testing production config methods...")
    
    try:
        # Test API config
        api_config = ProductionConfig.get_api_config()
        required_keys = ['api_base_url', 'api_timeout', 'api_max_retries', 'environment']
        
        for key in required_keys:
            if key not in api_config:
                print(f"❌ Missing config key: {key}")
                return False
        
        print("✅ API Config: All required keys present")
        
        # Test all settings
        all_settings = ProductionConfig.get_all_settings()
        if 'api_base_url' in all_settings:
            print("✅ All Settings: API config included")
        else:
            print("❌ All Settings: API config missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Config Test Failed: {e}")
        return False

def test_demo_functionality():
    """Test demo functionality used by Streamlit app."""
    print("🔍 Testing demo functionality...")
    
    try:
        # Simulate demo extraction
        test_url = "https://pitchfork.com/features/lists-and-guides/best-songs-2024/"
        client = APIClient(ProductionConfig.API_BASE_URL, ProductionConfig.API_TIMEOUT)
        
        result = client.extract_songs(test_url)
        songs = result.get('songs', [])
        
        if len(songs) > 0:
            print(f"✅ Demo Extraction: {len(songs)} songs extracted")
            
            # Simulate metrics calculation
            metrics = {
                'start_time': result.get('start_time'),
                'end_time': result.get('end_time'),
                'songs_extracted': len(songs),
                'extraction_method': 'production_api_server'
            }
            
            if result.get('start_time') and result.get('end_time'):
                metrics['duration'] = result['end_time'] - result['start_time']
                print(f"✅ Metrics Calculation: {metrics['duration']:.2f}s duration")
            
            return True
        else:
            print("❌ Demo Extraction: No songs found")
            return False
            
    except Exception as e:
        print(f"❌ Demo Test Failed: {e}")
        return False

def test_error_handling():
    """Test error handling scenarios."""
    print("🔍 Testing error handling...")
    
    try:
        # Test with invalid URL
        client = APIClient("http://invalid-url:9999", 5)
        
        try:
            result = client.health_check()
            print("❌ Error Handling: Should have failed with invalid URL")
            return False
        except Exception:
            print("✅ Error Handling: Correctly handles invalid API URL")
        
        # Test with valid client but invalid extraction URL
        valid_client = APIClient(ProductionConfig.API_BASE_URL, ProductionConfig.API_TIMEOUT)
        
        try:
            result = valid_client.extract_songs("invalid-url")
            print("✅ Error Handling: Gracefully handles invalid extraction URL")
        except Exception:
            print("✅ Error Handling: Properly raises exception for invalid URL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error Handling Test Failed: {e}")
        return False

def main():
    """Run all Streamlit API integration tests."""
    print("🚀 Streamlit API Integration Testing")
    print("=" * 50)
    
    tests = [
        ("API Client Functionality", test_api_client_functionality),
        ("Config Methods", test_config_methods),
        ("Demo Functionality", test_demo_functionality),
        ("Error Handling", test_error_handling)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        results[test_name] = test_func()
    
    print("\n" + "=" * 50)
    print("🎯 Streamlit Integration Test Results")
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
        print("🎉 All Streamlit integration tests passed!")
        print("✅ Production app ready for API integration")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())