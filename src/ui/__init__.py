"""
Streamlit UI components for the Netra space flight simulation platform.
"""

try:
    from .main_app import main
except ImportError:
    # Handle case where dependencies are not installed
    def main():
        print("Please install the required dependencies: pip install -r requirements.txt")

__all__ = ["main"]
