"""
Web Scraper Framework - Complete Integration
Sophisticated multi-site scraping framework with MCP browser integration
"""

from .unified_scraper import AccessibilityParser, UnifiedScraper
from .template_manager import SiteTemplate, TemplateManager
from .pattern_discovery import PatternDiscovery
from .real_mcp_browser import MCPBrowserAdapter
from .performance_optimizer import PerformanceOptimizer
from .site_expansion_toolkit import SiteExpansionToolkit

__all__ = [
    'AccessibilityParser',
    'UnifiedScraper', 
    'SiteTemplate',
    'TemplateManager',
    'PatternDiscovery',
    'MCPBrowserAdapter',
    'PerformanceOptimizer',
    'SiteExpansionToolkit'
]