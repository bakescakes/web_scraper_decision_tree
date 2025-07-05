"""
Site Expansion Toolkit - Simplified Railway Version
Provides site expansion utilities for Railway deployment
"""

from typing import List, Dict, Any, Optional
from urllib.parse import urlparse


class SiteExpansionToolkit:
    """Simplified site expansion toolkit for Railway deployment"""
    
    def __init__(self):
        self.supported_domains = {
            'pitchfork.com': {'type': 'editorial', 'priority': 'high'},
            'billboard.com': {'type': 'chart', 'priority': 'high'},
            'npr.org': {'type': 'editorial', 'priority': 'medium'},
            'theguardian.com': {'type': 'editorial', 'priority': 'medium'},
            'rollingstone.com': {'type': 'editorial', 'priority': 'medium'},
            'stereogum.com': {'type': 'editorial', 'priority': 'low'},
            'complex.com': {'type': 'complex_js', 'priority': 'medium'},
            'pastemagazine.com': {'type': 'editorial', 'priority': 'low'}
        }
    
    def analyze_domain(self, url: str) -> Dict[str, Any]:
        """Analyze domain for expansion potential"""
        domain = urlparse(url).netloc.lower()
        
        if domain in self.supported_domains:
            info = self.supported_domains[domain]
            return {
                'domain': domain,
                'supported': True,
                'type': info['type'],
                'priority': info['priority'],
                'expansion_potential': 'high' if info['priority'] == 'high' else 'medium'
            }
        else:
            return {
                'domain': domain,
                'supported': False,
                'type': 'unknown',
                'priority': 'unknown',
                'expansion_potential': 'low'
            }
    
    def suggest_similar_sites(self, url: str) -> List[str]:
        """Suggest similar sites for expansion"""
        domain = urlparse(url).netloc.lower()
        
        if domain in self.supported_domains:
            site_type = self.supported_domains[domain]['type']
            # Return sites of the same type
            similar = [d for d, info in self.supported_domains.items() 
                      if info['type'] == site_type and d != domain]
            return similar[:3]  # Return top 3
        else:
            return list(self.supported_domains.keys())[:3]
    
    def get_expansion_recommendations(self) -> List[Dict[str, Any]]:
        """Get recommendations for site expansion"""
        recommendations = []
        
        # High priority sites
        high_priority = [d for d, info in self.supported_domains.items() 
                        if info['priority'] == 'high']
        
        for domain in high_priority:
            recommendations.append({
                'domain': domain,
                'reason': 'High-value music site with large audience',
                'expected_benefit': 'High song extraction volume',
                'implementation_effort': 'Low (already supported)'
            })
        
        return recommendations