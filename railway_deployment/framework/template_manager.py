"""Template Manager for Music Site Scraping Framework - Part 1"""

import json
import os
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse


class SiteTemplate:
    """Represents a scraping template for a specific site pattern."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        
    def get_navigation_config(self) -> Dict[str, Any]:
        """Get navigation configuration for MCP browser."""
        return self.config.get('navigation', {})
    
    def get_container_config(self) -> Dict[str, Any]:
        """Get container identification configuration."""
        return self.config.get('container', {})
    
    def get_item_pattern(self) -> Dict[str, Any]:
        """Get item extraction pattern."""
        return self.config.get('item_pattern', {})
    
    def get_title_extraction(self) -> Dict[str, Any]:
        """Get title extraction configuration."""
        return self.config.get('title_extraction', {})
    
    def get_artist_extraction(self) -> Dict[str, Any]:
        """Get artist extraction configuration."""
        return self.config.get('artist_extraction', {})
    
    def get_metadata_fields(self) -> List[str]:
        """Get metadata field configuration."""
        return self.config.get('metadata_fields', [])


class TemplateManager:
    """Manages site templates and provides template matching functionality."""
    
    def __init__(self):
        self.templates = {}
        self.domain_mappings = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default templates from templates file or create defaults."""
        
        # Try to load from templates file first
        try:
            templates_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'site_templates.json')
            if os.path.exists(templates_file):
                self.import_templates(templates_file)
                return
        except Exception as e:
            print(f"Could not load templates file: {e}")
        
        # Fallback: Create basic default templates
        self._create_basic_templates()
    
    def _create_basic_templates(self):
        """Create basic default templates."""
        
        # Billboard-style template
        billboard_config = {
            'description': 'Template for Billboard charts',
            'navigation': {'method': 'direct_url', 'wait_for': 'main', 'timeout': 10},
            'container': {'role': 'main'},
            'item_pattern': {'role': 'list', 'nesting': 'deep'},
            'title_extraction': {'role': 'heading', 'level': 3},
            'artist_extraction': {'role': 'generic', 'position': 'after_title'},
            'metadata_fields': ['position', 'last_week', 'peak']
        }
        
        # Editorial-style template  
        editorial_config = {
            'description': 'Template for editorial music lists',
            'navigation': {'method': 'direct_url', 'wait_for': 'article', 'timeout': 10},
            'container': {'role': 'article'},
            'item_pattern': {'role': 'listitem', 'nesting': 'shallow'},
            'title_extraction': {'role': 'heading', 'level': [2, 3, 4]},
            'artist_extraction': {'role': 'generic', 'position': 'in_title'},
            'metadata_fields': ['description']
        }
        
        # Pitchfork-style template
        pitchfork_config = {
            'description': 'Template for Pitchfork lists',
            'navigation': {'method': 'direct_url', 'wait_for': 'main', 'timeout': 15},
            'container': {'role': 'main'},
            'item_pattern': {'role': 'listitem', 'nesting': 'moderate'},
            'title_extraction': {'role': 'heading', 'level': 2, 'position': 'sibling_after'},
            'artist_extraction': {'role': 'generic', 'position': 'in_title', 'format': 'Artist: "Song Title"'},
            'metadata_fields': ['ranking', 'year']
        }
        
        # Add templates
        self.templates['billboard_style'] = SiteTemplate('billboard_style', billboard_config)
        self.templates['editorial_style'] = SiteTemplate('editorial_style', editorial_config)
        self.templates['pitchfork_style'] = SiteTemplate('pitchfork_style', pitchfork_config)
        
        # Add domain mappings
        self.domain_mappings.update({
            'billboard.com': 'billboard_style',
            'pitchfork.com': 'pitchfork_style',
            'npr.org': 'editorial_style',
            'theguardian.com': 'editorial_style',
            'rollingstone.com': 'editorial_style'
        })
    
    def get_template_for_url(self, url: str) -> Optional[SiteTemplate]:
        """Get template for a given URL."""
        domain = urlparse(url).netloc.lower()
        template_name = self.domain_mappings.get(domain)
        if template_name:
            return self.templates.get(template_name)
        return None
    
    def get_all_templates(self) -> List[SiteTemplate]:
        """Get all available templates."""
        return list(self.templates.values())
    
    def get_template_for_domain(self, domain: str) -> Optional[SiteTemplate]:
        """Get template for a specific domain."""
        template_name = self.domain_mappings.get(domain)
        if template_name:
            return self.templates.get(template_name)
        return None
    
    def import_templates(self, filepath: str):
        """Import templates from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load templates
        for name, config in data.get('templates', {}).items():
            template = SiteTemplate(name, config)
            self.templates[name] = template
        
        # Load domain mappings
        self.domain_mappings.update(data.get('domain_mappings', {}))
        
        print(f"✅ Loaded {len(self.templates)} templates and {len(self.domain_mappings)} domain mappings")
