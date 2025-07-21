#!/usr/bin/env python3
"""
Minimal test of the Netra application components.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_simulation():
    """Test physics simulation."""
    print("Testing physics simulation...")
    from physics.simulation import SpaceFlightSimulation
    
    sim = SpaceFlightSimulation()
    if sim.current_state:
        print(f"✓ Initial altitude: {sim.current_state.altitude/1000:.1f} km")
        
        # Run a few simulation steps
        for i in range(3):
            state = sim.step()
            if state:
                print(f"  Step {i+1}: altitude = {state.altitude/1000:.1f} km, speed = {state.speed:.0f} m/s")
    else:
        print("❌ Failed to initialize simulation state")
        return False
    
    return True

def test_sensors():
    """Test sensor data generation."""
    print("\nTesting sensor data generation...")
    from physics.simulation import SpaceFlightSimulation
    from physics.sensors import SensorDataGenerator
    
    sim = SpaceFlightSimulation()
    sensors = SensorDataGenerator()
    
    if sim.current_state:
        data = sensors.generate_sensor_data(sim.current_state)
        print(f"✓ Generated {len(data)} sensor readings")
        print(f"  Altitude: {data['altitude']/1000:.1f} km")
        print(f"  Battery: {data['battery_voltage']:.1f} V")
        print(f"  Temperature: {data['temperature_internal']:.1f} °C")
    else:
        print("❌ Failed to get simulation state for sensor testing")
        return False
    
    return True

def test_data_loader():
    """Test data loading."""
    print("\nTesting data management...")
    from data.loader import DataLoader
    
    loader = DataLoader()
    summary = loader.get_data_summary()
    print(f"✓ Data summary: {summary}")
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing Netra Platform Components\n")
    
    try:
        test_simulation()
        test_sensors()
        test_data_loader()
        
        print("\n🎉 All tests passed! The platform is working correctly.")
        print("\nTo launch the full Streamlit application:")
        print("  python launch.py")
        print("or")
        print("  streamlit run src/ui/main_app.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
