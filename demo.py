#!/usr/bin/env python3
"""
Simple Streamlit demo to test the basic functionality.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure Streamlit
st.set_page_config(
    page_title="Netra Demo",
    page_icon="🚀",
    layout="wide"
)

def main():
    """Main demo function."""
    st.title("🚀 Netra Platform Demo")
    st.markdown("This is a simple demonstration of the Netra space flight simulation platform.")
    
    # Test basic imports
    try:
        from physics.simulation import SpaceFlightSimulation
        from physics.sensors import SensorDataGenerator
        from data.loader import DataLoader
        
        st.success("✅ All modules imported successfully!")
        
        # Create simulation
        sim = SpaceFlightSimulation()
        sensors = SensorDataGenerator()
        
        if sim.current_state:
            st.info(f"Initial altitude: {sim.current_state.altitude/1000:.1f} km")
            
            # Generate some sample data
            data_points = []
            for i in range(10):
                state = sim.step()
                if state:
                    sensor_data = sensors.generate_sensor_data(state)
                    data_points.append({
                        'time': i,
                        'altitude': state.altitude/1000,
                        'speed': state.speed,
                        'fuel': state.fuel_remaining,
                        'battery': sensor_data['battery_voltage']
                    })
            
            # Create DataFrame
            df = pd.DataFrame(data_points)
            
            # Display data
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Simulation Data")
                st.dataframe(df)
            
            with col2:
                st.subheader("📈 Altitude Chart")
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['time'],
                    y=df['altitude'],
                    mode='lines+markers',
                    name='Altitude (km)'
                ))
                fig.update_layout(
                    title="Spacecraft Altitude Over Time",
                    xaxis_title="Time (steps)",
                    yaxis_title="Altitude (km)"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Show system info
            st.subheader("🔧 System Information")
            st.write(f"**Simulation Steps:** {len(data_points)}")
            st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Platform Status:** Operational")
            
        else:
            st.error("❌ Failed to initialize simulation")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.write("Please check your installation and try again.")
        
        # Show error details
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
