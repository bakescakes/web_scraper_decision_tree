"""Shared site extraction patterns for both production and development environments."""

import re
from typing import Dict, List, Optional, Callable
from urllib.parse import urlparse

class SitePattern:
    """Individual site extraction pattern."""
    
    def __init__(self, name: str, pattern: str, format_func: Callable[[str], str] = None):
        self.name = name
        self.pattern = pattern
        self.format_func = format_func or (lambda x: x)
    
    def extract(self, text: str) -> List[str]:
        """Extract songs using this pattern."""
        matches = re.findall(self.pattern, text, re.IGNORECASE | re.MULTILINE)
        return [self.format_func(match) for match in matches if match]

class SitePatterns:
    """Collection of site-specific extraction patterns."""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, List[SitePattern]]:
        """Initialize site-specific patterns."""
        return {
            'pitchfork.com': [
                SitePattern(
                    'numbered_dash',
                    r'\d+\.\s*([^"]+?)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'quoted_title',
                    r'"([^"]+)"\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'artist_song_format',
                    r'([A-Za-z\s]+)\s*[-–]\s*"([^"]+)"',
                    lambda m: f"{m[0].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                )
            ],
            'rollingstone.com': [
                SitePattern(
                    'numbered_quotes',
                    r'\d+\.\s*["""]([^"""]+)["""].*?([A-Za-z\s]+)(?=\s*\d+\.|$)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'song_by_artist',
                    r'"([^"]+)"\s+by\s+([A-Za-z\s]+)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'generic_dash',
                    r'([A-Za-z\s]+)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[0].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                )
            ],
            'billboard.com': [
                SitePattern(
                    'chart_position',
                    r'(\d+)\s*([^"]+?)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[2].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'song_by_artist',
                    r'"([^"]+)"\s+by\s+([A-Za-z\s]+)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'hot_100_format',
                    r'(\d+)\s*([^"]+?)\s*,\s*([A-Za-z\s]+)',
                    lambda m: f"{m[2].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                )
            ],
            'genius.com': [
                SitePattern(
                    'song_by_artist',
                    r'"([^"]+)"\s+by\s+([A-Za-z\s]+)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'artist_song_dash',
                    r'([A-Za-z\s]+)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[0].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                )
            ],
            'npr.org': [
                SitePattern(
                    'numbered_list',
                    r'\d+\.\s*([^"]+?)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'song_by_artist',
                    r'"([^"]+)"\s+by\s+([A-Za-z\s]+)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                )
            ],
            'complex.com': [
                SitePattern(
                    'numbered_dash',
                    r'\d+\.\s*([^"]+?)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'hip_hop_format',
                    r'([A-Za-z\s]+)\s*[-–]\s*"([^"]+)"',
                    lambda m: f"{m[0].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                )
            ],
            'guardian.co.uk': [
                SitePattern(
                    'numbered_quotes',
                    r'\d+\.\s*([A-Za-z\s]+),\s*["""]([^"""]+)["""]',
                    lambda m: f"{m[0].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                ),
                SitePattern(
                    'artist_song_format',
                    r'([A-Za-z\s]+)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                    lambda m: f"{m[0].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
                )
            ]
        }
    
    def get_patterns_for_domain(self, domain: str) -> List[SitePattern]:
        """Get patterns for a specific domain."""
        # Normalize domain
        domain = domain.lower()
        
        # Try exact match first
        if domain in self.patterns:
            return self.patterns[domain]
        
        # Try partial matches
        for pattern_domain in self.patterns:
            if pattern_domain in domain or domain in pattern_domain:
                return self.patterns[pattern_domain]
        
        # Return generic patterns
        return self.get_generic_patterns()
    
    def get_generic_patterns(self) -> List[SitePattern]:
        """Get generic patterns that work across sites."""
        return [
            SitePattern(
                'generic_dash',
                r'([A-Za-z\s]+)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                lambda m: f"{m[0].strip()} - {m[1].strip()}" if isinstance(m, tuple) else m
            ),
            SitePattern(
                'generic_by',
                r'"([^"]+)"\s+by\s+([A-Za-z\s]+)',
                lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
            ),
            SitePattern(
                'generic_numbered',
                r'\d+\.\s*([^"]+?)\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
            ),
            SitePattern(
                'generic_quoted',
                r'"([^"]+)"\s*[-–]\s*([^"]+?)(?=\s*\d+\.|$)',
                lambda m: f"{m[1].strip()} - {m[0].strip()}" if isinstance(m, tuple) else m
            )
        ]
    
    def extract_songs_from_text(self, text: str, domain: str) -> List[str]:
        """Extract songs from text using appropriate patterns."""
        patterns = self.get_patterns_for_domain(domain)
        all_songs = []
        
        for pattern in patterns:
            try:
                songs = pattern.extract(text)
                all_songs.extend(songs)
            except Exception as e:
                # Continue with other patterns if one fails
                continue
        
        # Remove duplicates while preserving order
        seen = set()
        unique_songs = []
        for song in all_songs:
            if song and song not in seen:
                seen.add(song)
                unique_songs.append(song)
        
        return unique_songs
    
    def add_pattern(self, domain: str, pattern: SitePattern) -> None:
        """Add a new pattern for a domain."""
        if domain not in self.patterns:
            self.patterns[domain] = []
        self.patterns[domain].append(pattern)
    
    def get_all_domains(self) -> List[str]:
        """Get all supported domains."""
        return list(self.patterns.keys())

# Global instance
site_patterns = SitePatterns()