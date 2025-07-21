#!/usr/bin/env python3
"""
Setup script for the Netra space flight simulation platform.
"""

import os
import sys
import subprocess
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies."""
    logger.info("Installing dependencies...")
    
    try:
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Setup environment variables."""
    logger.info("Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_example.exists() and not env_file.exists():
        # Copy .env.example to .env
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        logger.info("Created .env file from .env.example")
    
    return True

def create_data_directories():
    """Create necessary data directories."""
    logger.info("Creating data directories...")
    
    directories = [
        "data/raw",
        "data/processed", 
        "data/synthetic",
        "data/chroma_db"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    return True

def initialize_sample_data():
    """Initialize sample data for demonstration."""
    logger.info("Initializing sample data...")
    
    try:
        # Add src to path for imports
        sys.path.insert(0, str(Path("src").absolute()))
        
        from src.data.loader import DataLoader
        from src.data.synthetic import SyntheticDataGenerator
        
        # Create sample mission documents
        loader = DataLoader()
        loader.create_sample_mission_data()
        
        # Generate synthetic data
        generator = SyntheticDataGenerator(seed=42)
        generator.save_synthetic_data("data/synthetic")
        
        logger.info("Sample data initialized successfully")
        return True
        
    except Exception as e:
        logger.warning(f"Failed to initialize sample data: {e}")
        logger.info("You can initialize sample data later by running the application")
        return True  # Don't fail setup for this

def run_tests():
    """Run basic tests to verify installation."""
    logger.info("Running basic tests...")
    
    try:
        # Test imports
        import streamlit
        import plotly
        import pandas
        import numpy
        
        logger.info("All core dependencies can be imported")
        
        # Test custom modules
        sys.path.insert(0, str(Path("src").absolute()))
        
        from src.physics.simulation import SpaceFlightSimulation
        from src.physics.sensors import SensorDataGenerator
        from src.rag.core import SpaceMissionRAG
        
        # Test basic functionality
        sim = SpaceFlightSimulation()
        sensor_gen = SensorDataGenerator()
        
        logger.info("All custom modules can be imported and instantiated")
        return True
        
    except Exception as e:
        logger.error(f"Tests failed: {e}")
        return False

def main():
    """Main setup function."""
    logger.info("Starting Netra platform setup...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Create directories
    if not create_data_directories():
        sys.exit(1)
    
    # Initialize sample data
    initialize_sample_data()
    
    # Run tests
    if not run_tests():
        logger.warning("Some tests failed, but setup will continue")
    
    logger.info("Setup completed successfully!")
    logger.info("You can now run the application with: streamlit run app.py")
    logger.info("Or use: python -m streamlit run src/ui/main_app.py")

if __name__ == "__main__":
    main()
