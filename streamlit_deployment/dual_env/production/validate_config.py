"""
Production configuration validation script
Validates that all components are properly configured for API integration
"""

import sys
import os
from typing import Dict, Any

def validate_configuration() -> Dict[str, Any]:
    """Validate production configuration and dependencies."""
    results = {
        'success': True,
        'errors': [],
        'warnings': [],
        'info': []
    }
    
    # Test imports
    try:
        from api_client import APIClient, APIConnectionError, APIExtractionError, check_api_health
        results['info'].append("✅ API client imports successful")
    except ImportError as e:
        results['errors'].append(f"❌ API client import failed: {e}")
        results['success'] = False
    
    try:
        from config import ProductionConfig
        results['info'].append("✅ Production config import successful")
        
        # Validate configuration values
        config = ProductionConfig.get_api_config()
        
        # Check API configuration
        if not config['api_base_url'].startswith('http'):
            results['errors'].append("❌ Invalid API base URL")
            results['success'] = False
        else:
            results['info'].append(f"✅ API Base URL: {config['api_base_url']}")
            
        if config['api_timeout'] < 10:
            results['warnings'].append("⚠️  API timeout seems low for production")
        else:
            results['info'].append(f"✅ API Timeout: {config['api_timeout']}s")
            
        results['info'].append(f"✅ Environment: {config['environment']}")
        results['info'].append(f"✅ Show Debug: {config['show_debug_info']}")
        
    except ImportError as e:
        results['errors'].append(f"❌ Config import failed: {e}")
        results['success'] = False
    
    # Test Streamlit
    try:
        import streamlit
        results['info'].append("✅ Streamlit import successful")
    except ImportError as e:
        results['errors'].append(f"❌ Streamlit import failed: {e}")
        results['success'] = False
    
    # Test requests
    try:
        import requests
        results['info'].append("✅ Requests library available")
    except ImportError as e:
        results['errors'].append(f"❌ Requests library missing: {e}")
        results['success'] = False
    
    return results

def main():
    """Main validation function."""
    print("🔍 Validating Production Configuration...")
    print("=" * 50)
    
    results = validate_configuration()
    
    # Print results
    for info in results['info']:
        print(info)
    
    for warning in results['warnings']:
        print(warning)
    
    for error in results['errors']:
        print(error)
    
    print("=" * 50)
    
    if results['success']:
        print("🎉 Configuration validation successful!")
        print("✅ Production environment ready for API integration")
        return 0
    else:
        print("❌ Configuration validation failed!")
        print("⚠️  Please fix the errors above before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())