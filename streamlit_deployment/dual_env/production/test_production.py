#!/usr/bin/env python3
"""
Production environment test script.
Validates the complete production system functionality.
"""

import sys
import os
import time
import json
from datetime import datetime

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from scraper import ProductionScraper, extract_songs_from_url
from config import ProductionConfig
from utils import DataValidator, URLAnalyzer, PerformanceTimer

def test_production_scraper():
    """Test the production scraper with real URLs."""
    print("🧪 PRODUCTION SCRAPER TEST")
    print("=" * 50)
    
    # Test URLs - using the validated Pitchfork URL from our previous work
    test_urls = [
        "https://pitchfork.com/features/lists-and-guides/best-songs-2024/",
        # Add more URLs as needed
    ]
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'config': ProductionConfig.get_performance_config(),
        'test_results': [],
        'overall_performance': {}
    }
    
    total_start_time = time.time()
    successful_tests = 0
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n📋 Test {i}/{len(test_urls)}: {URLAnalyzer.get_domain(url)}")
        print("-" * 30)
        
        with PerformanceTimer() as timer:
            try:
                # Test using the main function
                songs = extract_songs_from_url(url)
                
                # Validate results
                validation = DataValidator.validate_songs(songs)
                
                # Performance check
                duration = timer.elapsed()
                performance_status = "EXCELLENT" if duration < ProductionConfig.EXCELLENT_RESPONSE_TIME else \
                                   "GOOD" if duration < ProductionConfig.TARGET_RESPONSE_TIME else \
                                   "ACCEPTABLE" if duration < ProductionConfig.MAX_RESPONSE_TIME else \
                                   "SLOW"
                
                test_result = {
                    'url': url,
                    'domain': URLAnalyzer.get_domain(url),
                    'success': len(songs) > 0,
                    'songs_extracted': len(songs),
                    'duration_seconds': duration,
                    'performance_status': performance_status,
                    'validation': validation,
                    'sample_songs': songs[:5] if songs else [],
                    'meets_production_criteria': (
                        len(songs) >= ProductionConfig.MIN_SONGS_THRESHOLD and
                        duration < ProductionConfig.MAX_RESPONSE_TIME and
                        validation.get('valid_songs', 0) / max(len(songs), 1) >= ProductionConfig.QUALITY_THRESHOLD
                    )
                }
                
                results['test_results'].append(test_result)
                
                # Print results
                print(f"✅ Status: {'SUCCESS' if test_result['success'] else 'FAILED'}")
                print(f"🎵 Songs: {len(songs)}")
                print(f"⏱️  Duration: {duration:.2f}s ({performance_status})")
                print(f"📊 Quality: {validation['valid_songs']}/{validation['total_songs']} valid")
                print(f"🎯 Production Ready: {'YES' if test_result['meets_production_criteria'] else 'NO'}")
                
                if songs:
                    print(f"📝 Sample Songs:")
                    for j, song in enumerate(songs[:3], 1):
                        print(f"   {j}. {song}")
                
                if test_result['meets_production_criteria']:
                    successful_tests += 1
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                results['test_results'].append({
                    'url': url,
                    'domain': URLAnalyzer.get_domain(url),
                    'success': False,
                    'error': str(e),
                    'duration_seconds': timer.elapsed(),
                    'meets_production_criteria': False
                })
    
    total_duration = time.time() - total_start_time
    
    # Overall performance analysis
    results['overall_performance'] = {
        'total_duration': total_duration,
        'successful_tests': successful_tests,
        'total_tests': len(test_urls),
        'success_rate': successful_tests / len(test_urls) if test_urls else 0,
        'average_duration': total_duration / len(test_urls) if test_urls else 0,
        'production_ready': successful_tests > 0 and successful_tests / len(test_urls) >= 0.7
    }
    
    # Print summary
    print(f"\n🎯 PRODUCTION TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Successful tests: {successful_tests}/{len(test_urls)}")
    print(f"📊 Success rate: {results['overall_performance']['success_rate']:.1%}")
    print(f"⏱️  Average duration: {results['overall_performance']['average_duration']:.2f}s")
    print(f"🚀 Production ready: {'YES' if results['overall_performance']['production_ready'] else 'NO'}")
    
    # Save results
    results_file = f"production_test_results_{int(time.time())}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return results

def test_mcp_integration():
    """Test MCP browser integration if available."""
    print("\n🔧 MCP BROWSER INTEGRATION TEST")
    print("-" * 40)
    
    try:
        # Test if we're in an environment with MCP browser tools
        scraper = ProductionScraper()
        
        # This will test the MCP integration path vs fallback path
        test_url = "https://pitchfork.com/features/lists-and-guides/best-songs-2024/"
        
        print(f"Testing MCP integration with: {URLAnalyzer.get_domain(test_url)}")
        
        with PerformanceTimer() as timer:
            songs = scraper.extract_songs(test_url)
        
        duration = timer.elapsed()
        method = scraper.get_performance_metrics().get('extraction_method', 'unknown')
        
        print(f"✅ Extraction method: {method}")
        print(f"🎵 Songs extracted: {len(songs)}")
        print(f"⏱️  Duration: {duration:.2f}s")
        
        if method == 'mcp_browser':
            print("🎉 MCP browser tools are available and working!")
            return True
        else:
            print("⚠️  Using fallback method - MCP browser tools not available")
            return False
            
    except Exception as e:
        print(f"❌ MCP integration test failed: {str(e)}")
        return False

def main():
    """Main test function."""
    print("🏭 PRODUCTION ENVIRONMENT VALIDATION")
    print("=" * 60)
    print(f"Environment: {os.path.basename(os.path.dirname(__file__))}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Test MCP integration
    mcp_available = test_mcp_integration()
    
    # Test production scraper
    results = test_production_scraper()
    
    # Final assessment
    print(f"\n🏆 FINAL ASSESSMENT")
    print("=" * 50)
    
    if results['overall_performance']['production_ready']:
        print("✅ PRODUCTION ENVIRONMENT: READY")
        print("   • All core functionality working")
        print("   • Performance meets targets")
        print("   • Quality standards achieved")
        if mcp_available:
            print("   • MCP browser integration active")
        else:
            print("   • Fallback methods operational")
    else:
        print("❌ PRODUCTION ENVIRONMENT: NOT READY")
        print("   • Performance or quality issues detected")
        print("   • Review test results for specific problems")
    
    return results

if __name__ == "__main__":
    main()