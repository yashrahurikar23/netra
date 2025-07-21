#!/usr/bin/env python3
"""
Main entry point for the Netra space flight simulation platform.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point."""
    try:
        from src.ui.main_app import main as streamlit_main
        streamlit_main()
    except ImportError as e:
        print("Error: Required dependencies not installed.")
        print("Please run: pip install -r requirements.txt")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
