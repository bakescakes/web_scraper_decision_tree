"""Production web scraper tool - completely self-contained."""

import sys
import os
import time
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import re

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from config import ProductionConfig
from patterns import site_patterns
from utils import DataValidator, SongFormatter, URLAnalyzer, PerformanceTimer, Logger
from constants import PERFORMANCE_TARGETS, BROWSER_SETTINGS, MUSIC_SITES

# Configure logging
logger = Logger.setup_logger(__name__, ProductionConfig.LOG_LEVEL)

class ProductionScraper:
    """Production-ready web scraper with MCP browser integration."""
    
    def __init__(self):
        self.config = ProductionConfig()
        self.performance_metrics = {
            'start_time': None,
            'end_time': None,
            'songs_extracted': 0,
            'extraction_method': None
        }
        
    def extract_songs(self, url: str) -> List[str]:
        """
        Extract songs from URL using production-optimized MCP browser tools.
        
        Args:
            url: URL to extract songs from
            
        Returns:
            List of songs in "Artist - Song" format
        """
        self.performance_metrics['start_time'] = time.time()
        
        try:
            logger.info(f"Starting production extraction for: {url}")
            
            # Use MCP browser tools for extraction
            songs = self._extract_with_mcp_browser(url)
            
            self.performance_metrics['songs_extracted'] = len(songs)
            self.performance_metrics['extraction_method'] = 'mcp_browser'
            
            logger.info(f"Successfully extracted {len(songs)} songs")
            return songs
            
        except Exception as e:
            logger.error(f"Production extraction failed: {str(e)}")
            return []
            
        finally:
            self.performance_metrics['end_time'] = time.time()
            self._log_performance_metrics()
    
    def _extract_with_mcp_browser(self, url: str) -> List[str]:
        """
        Extract songs using MCP browser automation.
        
        This method uses the actual MCP browser tools available in the environment.
        """
        try:
            # Use the actual MCP browser tools available in this environment
            logger.info(f"Navigating to: {url}")
            
            # Step 1: Navigate to URL with optimized settings
            browser_navigate(url)
            
            # Step 2: Wait for content to load (optimized timing)
            logger.info("Waiting for content to load...")
            browser_wait_for(time=self.config.WAIT_TIME_SECONDS)
            
            # Step 3: Capture page snapshot
            logger.info("Capturing page snapshot...")
            snapshot = browser_snapshot()
            
            # Step 4: Extract songs from snapshot
            songs = self._extract_songs_from_snapshot(snapshot, url)
            
            logger.info(f"Successfully extracted {len(songs)} songs using MCP browser")
            return songs
            
        except NameError:
            # MCP browser tools not available in this environment
            logger.warning("MCP browser tools not available - running in test environment")
            return self._fallback_extraction(url)
        except Exception as e:
            logger.error(f"MCP browser extraction failed: {str(e)}")
            return self._fallback_extraction(url)
    
    def _extract_songs_from_snapshot(self, snapshot: Dict, url: str) -> List[str]:
        """
        Extract songs from browser snapshot using site-specific patterns.
        
        Args:
            snapshot: Browser accessibility snapshot
            url: Original URL for pattern matching
            
        Returns:
            List of songs in "Artist - Song" format
        """
        try:
            domain = URLAnalyzer.get_domain(url)
            
            # Extract text from snapshot
            snapshot_text = self._extract_text_from_snapshot(snapshot)
            
            # Use shared patterns for extraction
            songs = site_patterns.extract_songs_from_text(snapshot_text, domain)
            
            # Clean and format songs
            cleaned_songs = []
            for song in songs:
                cleaned = SongFormatter.clean_song_title(song)
                if cleaned and SongFormatter.validate_song_format(cleaned):
                    cleaned_songs.append(cleaned)
            
            # Validate extraction quality
            if DataValidator.is_valid_extraction(cleaned_songs):
                logger.info(f"High-quality extraction: {len(cleaned_songs)} songs from {domain}")
                return cleaned_songs
            else:
                logger.warning(f"Low-quality extraction from {domain}, trying generic patterns")
                # Try generic patterns as fallback
                generic_songs = site_patterns.extract_songs_from_text(snapshot_text, 'generic')
                generic_cleaned = [SongFormatter.clean_song_title(song) for song in generic_songs if song]
                
                # Return best result
                if DataValidator.is_valid_extraction(generic_cleaned):
                    return generic_cleaned
                elif len(cleaned_songs) > 0:
                    return cleaned_songs
                else:
                    return generic_cleaned
                
        except Exception as e:
            logger.error(f"Error extracting songs from snapshot: {str(e)}")
            return []
    
    def _extract_text_from_snapshot(self, snapshot: Dict) -> str:
        """Extract text content from browser snapshot using accessibility tree navigation."""
        try:
            def extract_text_recursive(element):
                """Recursively extract text from accessibility tree element."""
                text_parts = []
                
                if isinstance(element, dict):
                    # Get direct text if available
                    if 'text' in element:
                        text_parts.append(element['text'])
                    
                    # Process children recursively  
                    for key, value in element.items():
                        if key == 'children' and isinstance(value, list):
                            for child in value:
                                text_parts.extend(extract_text_recursive(child))
                        elif isinstance(value, list):
                            for item in value:
                                if isinstance(item, (dict, list)):
                                    text_parts.extend(extract_text_recursive(item))
                        elif isinstance(value, dict):
                            text_parts.extend(extract_text_recursive(value))
                            
                elif isinstance(element, list):
                    for item in element:
                        text_parts.extend(extract_text_recursive(item))
                elif isinstance(element, str):
                    text_parts.append(element)
                    
                return text_parts
            
            # Extract all text content
            all_text = extract_text_recursive(snapshot)
            full_text = '\n'.join(filter(None, all_text))
            
            logger.debug(f"Extracted {len(full_text)} characters from snapshot")
            return full_text
            
        except Exception as e:
            logger.error(f"Error extracting text from snapshot: {str(e)}")
            # Fallback: convert entire snapshot to string
            return str(snapshot) if snapshot else ""
    

    
    def _fallback_extraction(self, url: str) -> List[str]:
        """
        Fallback extraction method when MCP browser tools are not available.
        
        This uses traditional HTTP requests as a backup method.
        """
        logger.info(f"Attempting fallback extraction for: {url}")
        
        try:
            import requests
            
            # Make HTTP request with proper headers
            headers = {
                'User-Agent': BROWSER_SETTINGS['USER_AGENT']
            }
            
            response = requests.get(url, headers=headers, timeout=self.config.TIMEOUT_SECONDS)
            response.raise_for_status()
            
            # Extract text content
            from utils import TextProcessor
            text_content = TextProcessor.clean_text(response.text)
            
            # Get domain for pattern matching
            domain = URLAnalyzer.get_domain(url)
            
            # Extract songs using shared patterns
            songs = site_patterns.extract_songs_from_text(text_content, domain)
            
            # Clean and format songs
            cleaned_songs = []
            for song in songs:
                cleaned = SongFormatter.clean_song_title(song)
                if cleaned and SongFormatter.validate_song_format(cleaned):
                    cleaned_songs.append(cleaned)
            
            logger.info(f"Fallback extraction found {len(cleaned_songs)} valid songs")
            return cleaned_songs
            
        except Exception as e:
            logger.error(f"Fallback extraction failed: {str(e)}")
            return []
    
    def _log_performance_metrics(self):
        """Log performance metrics for monitoring."""
        if self.performance_metrics['start_time'] and self.performance_metrics['end_time']:
            duration = self.performance_metrics['end_time'] - self.performance_metrics['start_time']
            logger.info(f"Performance metrics: {duration:.2f}s, {self.performance_metrics['songs_extracted']} songs")
            
            if duration > self.config.MAX_RESPONSE_TIME:
                logger.warning(f"Response time exceeded target: {duration:.2f}s > {self.config.MAX_RESPONSE_TIME}s")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return self.performance_metrics.copy()


def extract_songs_from_url(url: str) -> List[str]:
    """
    Main entry point for production song extraction.
    
    Args:
        url: URL to extract songs from
        
    Returns:
        List of songs in "Artist - Song" format
    """
    scraper = ProductionScraper()
    return scraper.extract_songs(url)


if __name__ == "__main__":
    # Test the scraper
    test_url = "https://pitchfork.com/features/lists-and-guides/best-songs-2024/"
    songs = extract_songs_from_url(test_url)
    print(f"Extracted {len(songs)} songs:")
    for i, song in enumerate(songs[:10], 1):
        print(f"{i}. {song}")