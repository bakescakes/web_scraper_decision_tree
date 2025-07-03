"""Shared utilities for both production and development environments."""

import re
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class SongFormatter:
    """Utility class for formatting song titles."""
    
    @staticmethod
    def clean_song_title(song: str) -> str:
        """Clean and format song title."""
        if not song:
            return ""
        
        # Remove extra whitespace
        song = re.sub(r'\s+', ' ', song.strip())
        
        # Fix smart quotes
        song = song.replace('"', '"').replace('"', '"')
        song = song.replace(''', "'").replace(''', "'")
        
        # Remove common prefixes
        song = re.sub(r'^\d+\.\s*', '', song)  # Remove numbering
        song = re.sub(r'^[-–]\s*', '', song)   # Remove leading dashes
        
        return song.strip()
    
    @staticmethod
    def format_artist_song(artist: str, song: str) -> str:
        """Format artist and song into standard format."""
        artist = SongFormatter.clean_song_title(artist)
        song = SongFormatter.clean_song_title(song)
        
        if not artist or not song:
            return ""
        
        return f"{artist} - {song}"
    
    @staticmethod
    def parse_song_string(song_string: str) -> Optional[tuple]:
        """Parse a song string into (artist, song) tuple."""
        if not song_string:
            return None
        
        # Try different separators
        separators = [' - ', ' – ', ' by ', ' | ']
        
        for separator in separators:
            if separator in song_string:
                parts = song_string.split(separator, 1)
                if len(parts) == 2:
                    if separator == ' by ':
                        # "Song by Artist" format
                        return (parts[1].strip(), parts[0].strip())
                    else:
                        # "Artist - Song" format
                        return (parts[0].strip(), parts[1].strip())
        
        return None
    
    @staticmethod
    def validate_song_format(song: str) -> bool:
        """Validate if song is in correct format."""
        if not song:
            return False
        
        # Check for artist - song format
        if ' - ' in song:
            parts = song.split(' - ', 1)
            if len(parts) == 2 and all(part.strip() for part in parts):
                return True
        
        return False

class URLAnalyzer:
    """Utility class for analyzing URLs."""
    
    @staticmethod
    def get_domain(url: str) -> str:
        """Extract domain from URL."""
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except:
            return ""
    
    @staticmethod
    def is_music_site(url: str) -> bool:
        """Check if URL is from a known music site."""
        domain = URLAnalyzer.get_domain(url)
        
        music_domains = {
            'pitchfork.com',
            'rollingstone.com',
            'billboard.com',
            'genius.com',
            'npr.org',
            'complex.com',
            'guardian.co.uk',
            'stereogum.com',
            'pastemagazine.com',
            'spin.com',
            'allmusic.com',
            'metacritic.com',
            'consequenceofsound.net',
            'thefader.com',
            'nme.com'
        }
        
        return any(music_domain in domain for music_domain in music_domains)
    
    @staticmethod
    def get_site_type(url: str) -> str:
        """Determine site type from URL."""
        domain = URLAnalyzer.get_domain(url)
        
        if 'billboard.com' in domain:
            return 'chart'
        elif any(site in domain for site in ['pitchfork.com', 'rollingstone.com', 'npr.org']):
            return 'editorial'
        elif 'genius.com' in domain:
            return 'lyrics'
        elif any(site in domain for site in ['spotify.com', 'apple.com']):
            return 'streaming'
        else:
            return 'generic'

class PerformanceTimer:
    """Utility class for timing operations."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start timing."""
        self.start_time = time.time()
    
    def stop(self):
        """Stop timing."""
        self.end_time = time.time()
    
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

class DataValidator:
    """Utility class for validating extracted data."""
    
    @staticmethod
    def validate_songs(songs: List[str]) -> Dict[str, Any]:
        """Validate list of songs."""
        validation_results = {
            'total_songs': len(songs),
            'valid_songs': 0,
            'invalid_songs': 0,
            'empty_songs': 0,
            'duplicate_songs': 0,
            'validation_errors': []
        }
        
        if not songs:
            validation_results['validation_errors'].append("No songs provided")
            return validation_results
        
        seen_songs = set()
        
        for i, song in enumerate(songs):
            if not song or not song.strip():
                validation_results['empty_songs'] += 1
                validation_results['validation_errors'].append(f"Song {i+1}: Empty song")
                continue
            
            if song in seen_songs:
                validation_results['duplicate_songs'] += 1
                validation_results['validation_errors'].append(f"Song {i+1}: Duplicate song '{song}'")
                continue
            
            seen_songs.add(song)
            
            if SongFormatter.validate_song_format(song):
                validation_results['valid_songs'] += 1
            else:
                validation_results['invalid_songs'] += 1
                validation_results['validation_errors'].append(f"Song {i+1}: Invalid format '{song}'")
        
        return validation_results
    
    @staticmethod
    def is_valid_extraction(songs: List[str], min_songs: int = 1) -> bool:
        """Check if extraction is valid."""
        if len(songs) < min_songs:
            return False
        
        validation = DataValidator.validate_songs(songs)
        
        # Must have at least 70% valid songs
        if validation['total_songs'] > 0:
            valid_ratio = validation['valid_songs'] / validation['total_songs']
            return valid_ratio >= 0.7
        
        return False

class TextProcessor:
    """Utility class for text processing."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text for processing, with improved HTML handling."""
        if not text:
            return ""
        
        # Remove script and style content
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags but preserve text content
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Decode HTML entities
        import html
        text = html.unescape(text)
        
        # Remove CSS-like content
        text = re.sub(r'[a-zA-Z-]+:\s*[^;]+;', '', text)
        text = re.sub(r'rgba?\([^)]+\)', '', text)
        text = re.sub(r'#[0-9a-fA-F]{3,6}', '', text)
        text = re.sub(r'\d+px', '', text)
        text = re.sub(r'font-[a-zA-Z-]+', '', text)
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Remove lines that are mostly CSS/HTML artifacts
        lines = text.split('\n')
        clean_lines = []
        for line in lines:
            line = line.strip()
            # Skip lines that look like CSS/HTML artifacts
            if (line and 
                not re.match(r'^[a-zA-Z-]+:\s*[^;]+', line) and  # CSS properties
                not re.match(r'^[0-9.]+px|em|rem', line) and     # CSS measurements
                not re.match(r'^rgba?\(', line) and              # CSS colors
                len(line) > 5 and                                # Too short
                len(line) < 200):                                # Too long
                clean_lines.append(line)
        
        return '\n'.join(clean_lines).strip()
    
    @staticmethod
    def extract_text_blocks(text: str) -> List[str]:
        """Extract text blocks from content."""
        # Split by multiple newlines
        blocks = re.split(r'\n\s*\n', text)
        
        # Clean and filter blocks
        cleaned_blocks = []
        for block in blocks:
            cleaned = TextProcessor.clean_text(block)
            if cleaned and len(cleaned) > 10:  # Filter out very short blocks
                cleaned_blocks.append(cleaned)
        
        return cleaned_blocks
    
    @staticmethod
    def find_song_lists(text: str) -> List[str]:
        """Find potential song lists in text."""
        # Look for numbered lists
        numbered_lists = re.findall(r'(\d+\.\s*[^\n]+(?:\n\d+\.\s*[^\n]+)*)', text, re.MULTILINE)
        
        # Look for bulleted lists
        bulleted_lists = re.findall(r'([•\-*]\s*[^\n]+(?:\n[•\-*]\s*[^\n]+)*)', text, re.MULTILINE)
        
        return numbered_lists + bulleted_lists

class Logger:
    """Utility class for logging."""
    
    @staticmethod
    def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Set up a logger with consistent formatting."""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    @staticmethod
    def log_extraction_metrics(logger: logging.Logger, url: str, songs: List[str], duration: float):
        """Log extraction metrics."""
        logger.info(f"Extraction complete for {URLAnalyzer.get_domain(url)}")
        logger.info(f"Songs extracted: {len(songs)}")
        logger.info(f"Duration: {duration:.2f}s")
        
        if songs:
            validation = DataValidator.validate_songs(songs)
            logger.info(f"Valid songs: {validation['valid_songs']}/{validation['total_songs']}")
            
            if validation['validation_errors']:
                logger.warning(f"Validation errors: {len(validation['validation_errors'])}")

# Utility functions for backwards compatibility
def clean_song_title(song: str) -> str:
    """Clean and format song title."""
    return SongFormatter.clean_song_title(song)

def format_artist_song(artist: str, song: str) -> str:
    """Format artist and song into standard format."""
    return SongFormatter.format_artist_song(artist, song)

def get_domain(url: str) -> str:
    """Extract domain from URL."""
    return URLAnalyzer.get_domain(url)

def is_music_site(url: str) -> bool:
    """Check if URL is from a known music site."""
    return URLAnalyzer.is_music_site(url)

def validate_songs(songs: List[str]) -> Dict[str, Any]:
    """Validate list of songs."""
    return DataValidator.validate_songs(songs)