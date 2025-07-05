"""
Pattern Discovery for Music Site Scraping
Simplified version for Railway deployment
"""

import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


class PatternDiscovery:
    """Discovers and analyzes patterns in music site content"""
    
    def __init__(self):
        self.common_patterns = {
            'chart_indicators': ['hot', 'top', 'chart', 'best', 'billboard'],
            'song_indicators': ['song', 'track', 'single', 'hit'],
            'artist_indicators': ['artist', 'band', 'musician', 'performer'],
            'list_indicators': ['list', '100', '50', 'countdown', 'ranking']
        }
    
    def analyze_site(self, url: str) -> Dict[str, Any]:
        """Analyze a site URL for content patterns"""
        domain = urlparse(url).netloc.lower()
        
        analysis = {
            'domain': domain,
            'url': url,
            'predicted_type': self._predict_content_type(url),
            'expected_song_count': self._estimate_song_count(url),
            'extraction_strategy': self._suggest_strategy(url)
        }
        
        return analysis
    
    def _predict_content_type(self, url: str) -> str:
        """Predict the type of content based on URL patterns"""
        url_lower = url.lower()
        
        if any(indicator in url_lower for indicator in self.common_patterns['chart_indicators']):
            return 'chart'
        elif any(indicator in url_lower for indicator in self.common_patterns['list_indicators']):
            return 'list'
        elif 'review' in url_lower:
            return 'review'
        elif 'article' in url_lower or 'feature' in url_lower:
            return 'article'
        else:
            return 'unknown'
    
    def _estimate_song_count(self, url: str) -> int:
        """Estimate expected song count based on URL patterns"""
        url_lower = url.lower()
        
        # Look for numbers in URL
        numbers = re.findall(r'\d+', url)
        if numbers:
            largest_num = max(int(n) for n in numbers if int(n) <= 200)
            if largest_num >= 50:
                return largest_num
        
        # Pattern-based estimation
        if 'hot-100' in url_lower or 'top-100' in url_lower:
            return 100
        elif 'billboard-200' in url_lower:
            return 200
        elif any(indicator in url_lower for indicator in ['best', 'top', 'chart']):
            return 50
        elif 'review' in url_lower:
            return 12
        else:
            return 20
    
    def _suggest_strategy(self, url: str) -> str:
        """Suggest extraction strategy based on analysis"""
        content_type = self._predict_content_type(url)
        domain = urlparse(url).netloc.lower()
        
        if domain in ['pitchfork.com', 'billboard.com', 'npr.org']:
            return 'template_based'
        elif content_type == 'chart':
            return 'chart_extraction'
        elif content_type == 'list':
            return 'list_extraction'
        else:
            return 'generic_extraction'