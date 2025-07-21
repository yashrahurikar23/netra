#!/usr/bin/env python3
"""
Main entry point for Netra on Streamlit Community Cloud.
Optimized for free tier deployment.
"""

import os
import sys
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Set environment variables for deployment
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Launch the Netra application."""
    try:
        # Import and run the main app
        from ui.main_app import main as streamlit_main
        streamlit_main()
    except ImportError as e:
        import streamlit as st
        st.error(f"Import error: {e}")
        st.write("Please check that all dependencies are installed correctly.")
        st.code("pip install -r requirements.txt")
    except Exception as e:
        import streamlit as st
        st.error(f"Application error: {e}")
        st.write("Please check the logs for more details.")

if __name__ == "__main__":
    main()
