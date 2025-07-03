#!/usr/bin/env python3
"""
Test if MCP browser tools are available in the production environment.
"""

def test_mcp_browser_availability():
    """Test if MCP browser tools are available."""
    print("🔧 Testing MCP Browser Tool Availability")
    print("-" * 40)
    
    try:
        # Try to access browser tools
        browser_navigate("https://pitchfork.com/features/lists-and-guides/best-songs-2024/")
        print("✅ browser_navigate: Available")
        
        # Wait a moment
        browser_wait_for(time=1)
        print("✅ browser_wait_for: Available")
        
        # Take snapshot
        snapshot = browser_snapshot()
        print("✅ browser_snapshot: Available")
        print(f"📊 Snapshot type: {type(snapshot)}")
        print(f"📊 Snapshot keys: {list(snapshot.keys()) if isinstance(snapshot, dict) else 'Not a dict'}")
        
        return True, snapshot
        
    except NameError as e:
        print(f"❌ MCP browser tools not available: {str(e)}")
        return False, None
    except Exception as e:
        print(f"⚠️  MCP browser tools available but error occurred: {str(e)}")
        return True, None

def extract_sample_songs_from_snapshot(snapshot):
    """Extract sample songs from a real MCP snapshot."""
    if not snapshot:
        return []
    
    print("\n🎵 Extracting sample songs from MCP snapshot...")
    
    def extract_text_recursive(element):
        """Recursively extract text from accessibility tree."""
        text_parts = []
        
        if isinstance(element, dict):
            # Get direct text if available
            if 'text' in element:
                text_parts.append(element['text'])
            
            # Process children recursively  
            for key, value in element.items():
                if isinstance(value, list):
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
    
    # Extract all text
    all_text = extract_text_recursive(snapshot)
    
    # Look for song patterns in the text
    import re
    songs = []
    
    for text in all_text:
        if text and len(text) > 10 and len(text) < 100:
            # Look for patterns like "Artist: Song" or "Artist - Song"
            if ':' in text or '-' in text:
                # Clean and add potential songs
                cleaned = text.strip()
                if cleaned and not any(skip in cleaned.lower() for skip in ['advertisement', 'cookie', 'privacy', 'subscribe']):
                    songs.append(cleaned)
    
    # Remove duplicates and return first 10
    unique_songs = list(dict.fromkeys(songs))
    return unique_songs[:10]

def main():
    """Main test function."""
    print("🏭 MCP BROWSER INTEGRATION TEST")
    print("=" * 50)
    
    available, snapshot = test_mcp_browser_availability()
    
    if available and snapshot:
        print("\n🎉 MCP browser tools are working!")
        
        # Extract sample songs
        sample_songs = extract_sample_songs_from_snapshot(snapshot)
        
        if sample_songs:
            print(f"\n📝 Sample extracted content ({len(sample_songs)} items):")
            for i, song in enumerate(sample_songs, 1):
                print(f"   {i}. {song}")
        else:
            print("\n⚠️  No song-like content found in snapshot")
            
    elif available:
        print("\n⚠️  MCP browser tools available but snapshot failed")
    else:
        print("\n❌ MCP browser tools not available in this environment")
        print("   This means we're running in a standard Python environment")
        print("   Real MCP browser tools are only available in the agent environment")

if __name__ == "__main__":
    main()