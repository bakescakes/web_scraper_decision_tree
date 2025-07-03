"""
Main Streamlit App Entry Point for Cloud Deployment
Imports and runs the production Streamlit application
"""

import sys
import os
from pathlib import Path

# Add dual_env/production to path for imports
sys.path.append(str(Path(__file__).parent / "dual_env" / "production"))

# Import and run the production app
if __name__ == "__main__":
    from app import main
    main()