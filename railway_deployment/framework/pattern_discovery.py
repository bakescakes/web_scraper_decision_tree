"""
Pattern Discovery System for Music Site Scraping Framework
Simplified version for Railway deployment
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urlparse
from collections import Counter, defaultdict


class StructuralPattern:
    """Represents a discovered structural pattern in a site."""
    
    def __init__(self, pattern_type: str, confidence: float, data: Dict[str, Any]):
        self.pattern_type = pattern_type
        self.confidence = confidence
        self.data = data


class PatternDiscovery:
    """
    Automated analysis of sites to generate templates.
    Simplified version for Railway deployment.
    """
    
    def __init__(self, mcp_browser=None):
        self.mcp_browser = mcp_browser
        self.discovered_patterns = {}
        self.confidence_threshold = 0.7
        self.debug = False
    
    def analyze_site(self, url: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze a site and return template configuration with confidence.
        
        Args:
            url: URL to analyze
            
        Returns:
            Tuple of (template_config, confidence_score)
        """
        try:
            domain = urlparse(url).netloc.lower()
            
            # Use heuristic analysis for common music site patterns
            template_config, confidence = self._heuristic_analysis(url, domain)
            
            if self.debug:
                print(f"Pattern discovery for {domain}: confidence {confidence:.2f}")
            
            return template_config, confidence
            
        except Exception as e:
            if self.debug:
                print(f"Pattern discovery error for {url}: {e}")
            return self._get_generic_template(), 0.1
    
    def _heuristic_analysis(self, url: str, domain: str) -> Tuple[Dict[str, Any], float]:
        """Heuristic analysis based on URL patterns and domain knowledge."""
        
        url_lower = url.lower()
        
        # Billboard-style detection
        if any(keyword in domain for keyword in ['billboard', 'charts', 'chart']):
            return self._get_billboard_template(), 0.9
        
        # Pitchfork-style detection
        if any(keyword in domain for keyword in ['pitchfork']):
            return self._get_pitchfork_template(), 0.9
        
        # Editorial-style detection
        if any(keyword in domain for keyword in ['npr', 'guardian', 'rolling', 'stereogum', 'paste']):
            return self._get_editorial_template(), 0.8
        
        # Complex JS-style detection
        if any(keyword in domain for keyword in ['spotify', 'apple', 'complex', 'genius']):
            return self._get_complex_js_template(), 0.7
        
        # Music content detection from URL
        if any(keyword in url_lower for keyword in ['best-songs', 'top-songs', 'music', 'tracks', 'playlist']):
            # Default to editorial style for music content
            return self._get_editorial_template(), 0.6
        
        # Generic fallback
        return self._get_generic_template(), 0.3
    
    def _get_billboard_template(self) -> Dict[str, Any]:
        """Get Billboard-style template configuration."""
        return {
            'name': 'billboard_discovered',
            'description': 'Billboard-style chart template (discovered)',
            'navigation': {
                'method': 'direct_url',
                'wait_for': 'main',
                'timeout': 10
            },
            'container': {
                'role': 'main',
                'selector': 'main'
            },
            'item_pattern': {
                'role': 'list',
                'nesting': 'deep',
                'selector': 'list'
            },
            'title_extraction': {
                'role': 'heading',
                'level': 3,
                'attribute': 'name'
            },
            'artist_extraction': {
                'role': 'generic',
                'position': 'after_title',
                'attribute': 'name'
            },
            'metadata_fields': ['position', 'last_week', 'peak'],
            'expected_count_range': [50, 200]
        }
    
    def _get_pitchfork_template(self) -> Dict[str, Any]:
        """Get Pitchfork-style template configuration."""
        return {
            'name': 'pitchfork_discovered',
            'description': 'Pitchfork-style list template (discovered)',
            'navigation': {
                'method': 'direct_url',
                'wait_for': 'main',
                'timeout': 15
            },
            'container': {
                'role': 'main',
                'selector': 'main'
            },
            'item_pattern': {
                'role': 'listitem',
                'nesting': 'moderate',
                'selector': 'div.heading-h3'
            },
            'title_extraction': {
                'role': 'heading',
                'level': 2,
                'attribute': 'name',
                'position': 'sibling_after'
            },
            'artist_extraction': {
                'role': 'generic',
                'position': 'in_title',
                'attribute': 'name',
                'format': 'Artist: "Song Title"'
            },
            'metadata_fields': ['ranking', 'year'],
            'expected_count_range': [50, 100]
        }
    
    def _get_editorial_template(self) -> Dict[str, Any]:
        """Get editorial-style template configuration."""
        return {
            'name': 'editorial_discovered',
            'description': 'Editorial list template (discovered)',
            'navigation': {
                'method': 'direct_url',
                'wait_for': 'article',
                'timeout': 10
            },
            'container': {
                'role': 'article',
                'selector': 'article'
            },
            'item_pattern': {
                'role': 'listitem',
                'nesting': 'shallow',
                'selector': 'listitem'
            },
            'title_extraction': {
                'role': 'heading',
                'level': [2, 3, 4],
                'attribute': 'name'
            },
            'artist_extraction': {
                'role': 'generic',
                'position': 'in_title',
                'attribute': 'name'
            },
            'metadata_fields': ['description'],
            'expected_count_range': [10, 50]
        }
    
    def _get_complex_js_template(self) -> Dict[str, Any]:
        """Get complex JavaScript template configuration."""
        return {
            'name': 'complex_js_discovered',
            'description': 'Complex JS site template (discovered)',
            'navigation': {
                'method': 'browser_automation',
                'wait_for': 'loaded',
                'timeout': 20,
                'scroll_required': True
            },
            'container': {
                'role': 'main',
                'selector': 'main'
            },
            'item_pattern': {
                'role': 'listitem',
                'nesting': 'variable',
                'selector': 'dynamic'
            },
            'title_extraction': {
                'role': 'heading',
                'level': [2, 3],
                'attribute': 'name'
            },
            'artist_extraction': {
                'role': 'generic',
                'position': 'context_dependent',
                'attribute': 'name'
            },
            'metadata_fields': ['dynamic_metadata'],
            'expected_count_range': [10, 100]
        }
    
    def _get_generic_template(self) -> Dict[str, Any]:
        """Get generic fallback template configuration."""
        return {
            'name': 'generic_discovered',
            'description': 'Generic site template (discovered)',
            'navigation': {
                'method': 'direct_url',
                'wait_for': 'main',
                'timeout': 10
            },
            'container': {
                'role': 'main',
                'selector': 'main'
            },
            'item_pattern': {
                'role': 'generic',
                'nesting': 'unknown',
                'selector': 'generic'
            },
            'title_extraction': {
                'role': 'heading',
                'level': [1, 2, 3],
                'attribute': 'name'
            },
            'artist_extraction': {
                'role': 'generic',
                'position': 'unknown',
                'attribute': 'name'
            },
            'metadata_fields': [],
            'expected_count_range': [1, 50]
        }
    
    def enable_debug(self):
        """Enable debug mode."""
        self.debug = True
    
    def get_discovered_patterns(self) -> Dict[str, Any]:
        """Get all discovered patterns."""
        return self.discovered_patterns.copy()
    
    def save_pattern(self, url: str, pattern: StructuralPattern):
        """Save a discovered pattern for future use."""
        domain = urlparse(url).netloc.lower()
        self.discovered_patterns[domain] = {
            'pattern_type': pattern.pattern_type,
            'confidence': pattern.confidence,
            'data': pattern.data,
            'discovered_at': url
        }
    
    def get_pattern_for_domain(self, domain: str) -> Optional[StructuralPattern]:
        """Get previously discovered pattern for domain."""
        pattern_data = self.discovered_patterns.get(domain)
        if pattern_data:
            return StructuralPattern(
                pattern_data['pattern_type'],
                pattern_data['confidence'], 
                pattern_data['data']
            )
        return None


# Example usage
if __name__ == "__main__":
    # Test pattern discovery
    discovery = PatternDiscovery()
    discovery.enable_debug()
    
    test_urls = [
        "https://www.billboard.com/charts/hot-100/",
        "https://pitchfork.com/features/lists-and-guides/best-songs-2024/",
        "https://www.npr.org/2023/12/14/1218902324/best-songs-2023",
        "https://www.theguardian.com/music/2023/dec/12/the-20-best-songs-of-2023",
        "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF"
    ]
    
    for url in test_urls:
        print(f"\nAnalyzing: {url}")
        template_config, confidence = discovery.analyze_site(url)
        print(f"Template: {template_config['name']}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Description: {template_config['description']}")
        print("---")