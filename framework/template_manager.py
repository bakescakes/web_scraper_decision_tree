"""
Template Manager for Music Site Scraping Framework
Simplified version for Railway deployment
"""

import json
import os
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse


class SiteTemplate:
    """Represents a scraping template for a specific site pattern."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config


class TemplateManager:
    """Manages site templates and provides template matching functionality."""
    
    def __init__(self):
        self.templates = {}
        self.domain_mappings = {
            'pitchfork.com': 'editorial_style',
            'billboard.com': 'billboard_style',
            'npr.org': 'editorial_style',
            'theguardian.com': 'editorial_style',
            'rollingstone.com': 'editorial_style',
            'stereogum.com': 'editorial_style',
            'complex.com': 'complex_js_style',
            'pastemagazine.com': 'editorial_style',
            'consequence.net': 'editorial_style',
            'spin.com': 'editorial_style',
            'musicblog.org': 'editorial_style'
        }
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default templates"""
        
        # Billboard-style template
        self.templates['billboard_style'] = SiteTemplate('billboard_style', {
            'description': 'Billboard chart-style template with numbered lists',
            'song_count': 100,
            'patterns': ['Artist - Song Title']
        })
        
        # Editorial-style template
        self.templates['editorial_style'] = SiteTemplate('editorial_style', {
            'description': 'Editorial content with article-style song lists',
            'song_count': 25,
            'patterns': ['Artist - Song', 'Song by Artist']
        })
        
        # Complex JS template
        self.templates['complex_js_style'] = SiteTemplate('complex_js_style', {
            'description': 'Complex sites with JavaScript-heavy content',
            'song_count': 20,
            'patterns': ['Artist - Song Title']
        })
        
        # Generic template
        self.templates['generic'] = SiteTemplate('generic', {
            'description': 'Generic template for unknown sites',
            'song_count': 15,
            'patterns': ['Artist - Song']
        })
    
    def get_template_for_url(self, url: str) -> Optional[SiteTemplate]:
        """Get the best template for a given URL"""
        domain = urlparse(url).netloc.lower()
        
        # Check domain mappings
        template_name = self.domain_mappings.get(domain)
        if template_name and template_name in self.templates:
            return self.templates[template_name]
        
        # Fallback to generic
        return self.templates.get('generic')
    
    def get_all_templates(self) -> List[SiteTemplate]:
        """Get all available templates"""
        return list(self.templates.values())
    
    def get_domains_for_template(self, template_name: str) -> List[str]:
        """Get domains that use a specific template"""
        return [domain for domain, tmpl in self.domain_mappings.items() if tmpl == template_name]