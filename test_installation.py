#!/usr/bin/env python3
"""Simple test script to verify installation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test basic imports."""
    try:
        import streamlit
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import plotly
        print("✓ Plotly imported successfully")
    except ImportError as e:
        print(f"✗ Plotly import failed: {e}")
        return False
    
    try:
        import numpy
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import pandas
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test custom module imports."""
    try:
        from physics.simulation import SpaceFlightSimulation
        print("✓ Physics simulation module imported successfully")
        
        from physics.sensors import SensorDataGenerator
        print("✓ Sensor data module imported successfully")
        
        from rag.core import SpaceMissionRAG
        print("✓ RAG core module imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Custom module import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality."""
    try:
        from physics.simulation import SpaceFlightSimulation
        sim = SpaceFlightSimulation()
        print("✓ Simulation object created successfully")
        
        from physics.sensors import SensorDataGenerator
        sensors = SensorDataGenerator()
        print("✓ Sensor generator created successfully")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Netra platform installation...\n")
    
    print("1. Testing basic imports:")
    if not test_imports():
        print("\nInstallation incomplete. Please install missing dependencies.")
        sys.exit(1)
    
    print("\n2. Testing custom modules:")
    if not test_custom_modules():
        print("\nCustom modules have issues. Check the implementation.")
        sys.exit(1)
    
    print("\n3. Testing basic functionality:")
    if not test_basic_functionality():
        print("\nBasic functionality test failed.")
        sys.exit(1)
    
    print("\n🎉 All tests passed! Netra platform is ready to use.")
    print("\nTo start the application, run:")
    print("  streamlit run app.py")
    print("or")
    print("  python -m streamlit run src/ui/main_app.py")
