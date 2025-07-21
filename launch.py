#!/usr/bin/env python3
"""
Launch script for the Netra application.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Netra application."""
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Check if in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment detected")
    else:
        print("⚠️  No virtual environment detected. Consider using one.")
    
    # Launch Streamlit
    print("🚀 Starting Netra platform...")
    print("The application will open in your web browser at http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            sys.executable, 
            "-m", "streamlit", "run", 
            "src/ui/main_app.py",
            "--server.headless=true",
            "--server.port=8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    main()
