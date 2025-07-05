"""
API Client for MCP API Server
Development environment client for connecting to the MCP API server
"""

import requests
import time
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin
import json

logger = logging.getLogger(__name__)

class APIClient:
    """HTTP client for the MCP API server"""
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 60):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the MCP API server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Configure session
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'MCP-API-Client/1.0'
        })
        
        # Store last request performance
        self.last_request_time = None
        self.last_response_time = None
        
    def health_check(self) -> Dict[str, Any]:
        """
        Check API server health
        
        Returns:
            Health check response
        """
        try:
            start_time = time.time()
            response = self.session.get(
                urljoin(self.base_url, "/health"),
                timeout=self.timeout
            )
            end_time = time.time()
            
            self.last_request_time = start_time
            self.last_response_time = end_time
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Health check failed: {str(e)}")
            raise APIConnectionError(f"Failed to connect to API server: {str(e)}")
    
    def extract_songs(self, url: str, timeout: int = 60, max_retries: int = 3) -> Dict[str, Any]:
        """
        Extract songs from URL using the API
        
        Args:
            url: URL to extract songs from
            timeout: Request timeout
            max_retries: Maximum retries for extraction
            
        Returns:
            Extraction results
        """
        try:
            start_time = time.time()
            
            # Prepare request parameters for GET request
            params = {
                "url": url
            }
            
            # Add optional parameters if provided
            if timeout != 60:  # Only add if different from default
                params["timeout"] = timeout
            if max_retries != 3:  # Only add if different from default
                params["max_retries"] = max_retries
            
            # Make API request using GET method with query parameters
            response = self.session.get(
                urljoin(self.base_url, "/extract"),
                params=params,
                timeout=self.timeout
            )
            
            end_time = time.time()
            
            self.last_request_time = start_time
            self.last_response_time = end_time
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Successfully extracted {len(result.get('songs', []))} songs in {end_time - start_time:.2f}s")
            return result
            
        except requests.RequestException as e:
            logger.error(f"Song extraction failed: {str(e)}")
            
            # Try to get error details from response
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    raise APIExtractionError(f"API extraction failed: {error_detail.get('detail', str(e))}")
                except json.JSONDecodeError:
                    raise APIExtractionError(f"API extraction failed: {str(e)}")
            else:
                raise APIConnectionError(f"Failed to connect to API server: {str(e)}")
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get server information
        
        Returns:
            Server information
        """
        try:
            response = self.session.get(
                urljoin(self.base_url, "/"),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Failed to get server info: {str(e)}")
            raise APIConnectionError(f"Failed to connect to API server: {str(e)}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the last request
        
        Returns:
            Performance metrics
        """
        if self.last_request_time and self.last_response_time:
            return {
                'start_time': self.last_request_time,
                'end_time': self.last_response_time,
                'duration': self.last_response_time - self.last_request_time,
                'extraction_method': 'api_server'
            }
        return {}
    
    def test_connection(self) -> bool:
        """
        Test connection to API server
        
        Returns:
            True if connection successful
        """
        try:
            health = self.health_check()
            # Accept both 'healthy' and 'degraded' status as valid connections
            status = health.get('status')
            return status in ['healthy', 'degraded']
        except Exception:
            return False


class APIConnectionError(Exception):
    """Exception raised when API connection fails"""
    pass


class APIExtractionError(Exception):
    """Exception raised when API extraction fails"""
    pass


# Convenience functions for easy integration
def extract_songs_from_url(url: str, api_base_url: str = "http://localhost:8000") -> List[str]:
    """
    Convenience function to extract songs from URL
    
    Args:
        url: URL to extract songs from
        api_base_url: Base URL of the API server
        
    Returns:
        List of songs
    """
    client = APIClient(api_base_url)
    try:
        result = client.extract_songs(url)
        return result.get('songs', [])
    except Exception as e:
        logger.error(f"Failed to extract songs: {str(e)}")
        raise


def check_api_health(api_base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Convenience function to check API health
    
    Args:
        api_base_url: Base URL of the API server
        
    Returns:
        Health check result
    """
    client = APIClient(api_base_url)
    return client.health_check()


# Mock scraper class for compatibility with existing code
class ProductionScraper:
    """Mock scraper that uses API client for compatibility"""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_client = APIClient(api_base_url)
        self.performance_metrics = {}
        
    def extract_songs(self, url: str) -> List[str]:
        """Extract songs using API client"""
        try:
            result = self.api_client.extract_songs(url)
            
            # Store metrics
            self.performance_metrics = {
                'start_time': result.get('start_time'),
                'end_time': result.get('end_time'),
                'songs_extracted': len(result.get('songs', [])),
                'extraction_method': 'api_server'
            }
            
            return result.get('songs', [])
            
        except Exception as e:
            logger.error(f"API extraction failed: {str(e)}")
            raise
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.performance_metrics