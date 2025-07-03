"""
Production Streamlit app with API integration
Updated to use MCP API server instead of direct MCP integration
"""

import streamlit as st
import time
import sys
import os
from typing import List, Dict, Any
import logging

# Import API client and config
from api_client import APIClient, APIConnectionError, APIExtractionError, check_api_health
from config import ProductionConfig

# Configure logging
logging.basicConfig(level=getattr(logging, ProductionConfig.LOG_LEVEL))
logger = logging.getLogger(__name__)

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title=ProductionConfig.STREAMLIT_CONFIG['PAGE_TITLE'],
        page_icon=ProductionConfig.STREAMLIT_CONFIG['PAGE_ICON'],
        layout=ProductionConfig.STREAMLIT_CONFIG['LAYOUT']
    )
    
    st.title("🎵 Music List Extractor - Production")
    st.markdown("Extract song lists from music websites using the production MCP API server.")
    
    # API Status Section
    if ProductionConfig.SHOW_API_STATUS:
        display_api_status()
    
    # Demo section
    if ProductionConfig.ENABLE_DEMO_MODE:
        with st.expander("🎯 Try the Demo - Production API Integration", expanded=True):
            st.markdown("""
            **Click below to test the production API integration!**
            
            This demo connects to the MCP API server and extracts songs from a validated URL:
            """)
            
            demo_url = "https://pitchfork.com/features/lists-and-guides/best-songs-2024/"
            
            if st.button("🚀 Run Production API Demo", type="primary"):
                run_api_demo(demo_url)
    
    # Input section for custom URLs
    st.header("Extract from Custom URL")
    url = st.text_input(
        "Enter music list URL:",
        placeholder="https://pitchfork.com/features/lists-and-guides/best-songs-2024/",
        help="Enter a URL from a music website containing a list of songs"
    )
    
    if url:
        if st.button("Extract Songs via API", type="secondary"):
            extract_and_display_songs(url)
    
    # API Configuration section
    if ProductionConfig.SHOW_DEBUG_INFO:
        st.header("API Configuration")
        display_api_config()
    
    # Information section
    st.header("How It Works")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔧 Architecture:**
        - Production API-first design
        - Standalone MCP server
        - HTTP client integration
        - Optimized for reliability
        """)
    
    with col2:
        st.markdown("""
        **📊 Performance:**
        - Target: <15 seconds
        - Maximum: <40 seconds
        - Quality threshold: 70%
        - Minimum songs: 5
        """)
    
    # Supported sites
    st.header("Supported Sites")
    supported_sites = [
        "🎵 Pitchfork", "🎸 Rolling Stone", "📊 Billboard", "🎤 Genius",
        "📻 NPR Music", "🌆 Complex", "📰 The Guardian", "🎶 Stereogum",
        "📝 Paste Magazine", "🎭 Spin", "💿 AllMusic", "⭐ Metacritic"
    ]
    
    cols = st.columns(4)
    for i, site in enumerate(supported_sites):
        with cols[i % 4]:
            st.markdown(f"- {site}")
    
    # Performance metrics
    if 'last_metrics' in st.session_state:
        st.header("Last Extraction Performance")
        display_performance_metrics(st.session_state.last_metrics)

def display_api_status():
    """Display API server status"""
    st.header("🔗 API Server Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            health = check_api_health(ProductionConfig.API_BASE_URL)
            if health.get('status') == 'healthy':
                st.success("✅ API Server Online")
            elif health.get('status') == 'degraded':
                st.warning("⚠️ API Server Degraded (HTTP mode)")
            else:
                st.warning("⚠️ API Server Issues")
        except Exception:
            st.error("❌ API Server Offline")
    
    with col2:
        st.info(f"📡 {ProductionConfig.API_BASE_URL}")
    
    with col3:
        st.info(f"⏱️ Timeout: {ProductionConfig.API_TIMEOUT}s")
    
    # Detailed health check
    with st.expander("🔍 Detailed API Status", expanded=False):
        try:
            health = check_api_health(ProductionConfig.API_BASE_URL)
            st.json(health)
        except Exception as e:
            st.error(f"Failed to get API status: {str(e)}")

def display_api_config():
    """Display API configuration"""
    config = ProductionConfig.get_api_config()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**API Settings:**")
        st.code(f"""
API Base URL: {config['api_base_url']}
Timeout: {config['api_timeout']}s
Max Retries: {config['api_max_retries']}
Environment: {config['environment']}
        """)
    
    with col2:
        st.markdown("**Performance Targets:**")
        st.code(f"""
Target Response: {ProductionConfig.TARGET_RESPONSE_TIME}s
Max Response: {ProductionConfig.MAX_RESPONSE_TIME}s
Min Songs: {ProductionConfig.MIN_SONGS_THRESHOLD}
Quality Threshold: {ProductionConfig.QUALITY_THRESHOLD}
        """)

def extract_and_display_songs(url: str):
    """Extract and display songs from URL using API."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize API client
        client = APIClient(ProductionConfig.API_BASE_URL, ProductionConfig.API_TIMEOUT)
        
        # Update progress
        progress_bar.progress(25)
        status_text.text("Connecting to production API server...")
        
        # Test connection
        if not client.test_connection():
            st.error("❌ Cannot connect to API server. Please ensure it's running.")
            return
        
        # Extract songs
        progress_bar.progress(50)
        status_text.text("Extracting songs via production API...")
        
        result = client.extract_songs(
            url, 
            timeout=ProductionConfig.API_TIMEOUT,
            max_retries=ProductionConfig.API_MAX_RETRIES
        )
        
        songs = result.get('songs', [])
        
        progress_bar.progress(75)
        status_text.text("Formatting results...")
        
        # Display results
        progress_bar.progress(100)
        status_text.text("Complete!")
        
        # Store metrics
        metrics = {
            'start_time': result.get('start_time'),
            'end_time': result.get('end_time'),
            'songs_extracted': len(songs),
            'extraction_method': 'production_api_server'
        }
        
        if result.get('start_time') and result.get('end_time'):
            metrics['duration'] = result['end_time'] - result['start_time']
        
        st.session_state.last_metrics = metrics
        
        if songs:
            st.success(f"✅ Successfully extracted {len(songs)} songs via production API!")
            
            # Display songs
            st.header("🎵 Extracted Songs")
            for i, song in enumerate(songs, 1):
                st.write(f"{i}. {song}")
            
            # Show API response details (only if debug enabled)
            if ProductionConfig.SHOW_DEBUG_INFO:
                with st.expander("📋 API Response Details", expanded=False):
                    st.json(result)
            
            # Download option
            song_text = "\n".join(f"{i}. {song}" for i, song in enumerate(songs, 1))
            st.download_button(
                label="📥 Download Song List",
                data=song_text,
                file_name=f"songs_{int(time.time())}.txt",
                mime="text/plain"
            )
            
        else:
            st.error("No songs found. The URL may not be supported or may be temporarily unavailable.")
            
    except APIConnectionError as e:
        st.error(f"❌ API Connection Error: {str(e)}")
        st.info("💡 Make sure the MCP API server is running on the configured URL.")
        
    except APIExtractionError as e:
        st.error(f"❌ API Extraction Error: {str(e)}")
        
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected extraction error: {str(e)}")
        
    finally:
        progress_bar.empty()
        status_text.empty()

def run_api_demo(demo_url: str):
    """Run a demo extraction using the production API."""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("🔗 Connecting to production API server...")
        progress_bar.progress(25)
        
        # Initialize API client
        client = APIClient(ProductionConfig.API_BASE_URL, ProductionConfig.API_TIMEOUT)
        
        # Test connection
        if not client.test_connection():
            st.error("❌ Cannot connect to API server. Please ensure it's running.")
            return
        
        status_text.text("🎯 Running production API demo extraction...")
        progress_bar.progress(50)
        
        # Extract songs via API
        result = client.extract_songs(demo_url)
        songs = result.get('songs', [])
        
        progress_bar.progress(75)
        status_text.text("✅ Production API extraction complete!")
        
        # Calculate metrics
        metrics = {
            'start_time': result.get('start_time'),
            'end_time': result.get('end_time'),
            'songs_extracted': len(songs),
            'extraction_method': 'production_api_server'
        }
        
        if result.get('start_time') and result.get('end_time'):
            metrics['duration'] = result['end_time'] - result['start_time']
            duration_text = f" in {metrics['duration']:.2f}s"
        else:
            duration_text = ""
        
        progress_bar.progress(100)
        
        # Store metrics
        st.session_state.last_metrics = metrics
        
        # Display results
        if songs:
            st.success(f"🎉 Production API Demo complete! Extracted {len(songs)} songs{duration_text}")
            
            st.header("🎵 Extracted Songs (via Production API)")
            for i, song in enumerate(songs, 1):
                st.write(f"{i}. {song}")
            
            # Show API response details (only if debug enabled)
            if ProductionConfig.SHOW_DEBUG_INFO:
                with st.expander("📋 API Response Details", expanded=False):
                    st.json(result)
            
            # Download option
            song_text = "\n".join(f"{i}. {song}" for i, song in enumerate(songs, 1))
            st.download_button(
                label="📥 Download Song List",
                data=song_text,
                file_name=f"pitchfork_best_songs_2024_production_api.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ No songs extracted. Check API server logs for details.")
            
    except APIConnectionError as e:
        st.error(f"❌ API Connection Error: {str(e)}")
        st.info("💡 Make sure the MCP API server is running on the configured URL.")
        
    except APIExtractionError as e:
        st.error(f"❌ API Extraction Error: {str(e)}")
        
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected demo error: {str(e)}")
        
    finally:
        progress_bar.empty()
        status_text.empty()

def display_performance_metrics(metrics: Dict[str, Any]):
    """Display performance metrics in a nice format."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if metrics.get('duration'):
            duration = metrics['duration']
            st.metric(
                "⏱️ Duration", 
                f"{duration:.2f}s",
                help=f"Target: <{ProductionConfig.TARGET_RESPONSE_TIME}s"
            )
        else:
            st.metric("⏱️ Duration", "N/A")
    
    with col2:
        songs_count = metrics.get('songs_extracted', 0)
        st.metric(
            "🎵 Songs", 
            songs_count,
            help=f"Minimum: {ProductionConfig.MIN_SONGS_THRESHOLD} songs"
        )
    
    with col3:
        method = metrics.get('extraction_method', 'unknown')
        method_display = {
            'production_api_server': '🚀 Production API',
            'api_server': '🌐 API Server',
            'mcp_browser': '🌐 MCP Browser',
            'fallback': '🔄 HTTP Fallback',
            'unknown': '❓ Unknown'
        }.get(method, method)
        st.metric("🔧 Method", method_display)
    
    with col4:
        # Calculate quality status
        if songs_count >= 10:
            quality = "Excellent"
        elif songs_count >= ProductionConfig.MIN_SONGS_THRESHOLD:
            quality = "Good"
        else:
            quality = "Poor"
        st.metric("📊 Quality", quality)

if __name__ == "__main__":
    main()