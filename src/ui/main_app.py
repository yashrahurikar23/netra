"""
Main Streamlit application for Netra space flight simulation platform.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Import our modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.simulation import SpaceFlightSimulation, SimulationParameters, SimulationState
from physics.sensors import SensorDataGenerator
from rag.core import SpaceMissionRAG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Netra - Space Flight Simulation & RAG Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.25rem 0;
    }
    .simulation-status {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-active {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .status-inactive {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'simulation' not in st.session_state:
        st.session_state.simulation = SpaceFlightSimulation()
    
    if 'sensor_generator' not in st.session_state:
        st.session_state.sensor_generator = SensorDataGenerator()
    
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None  # Will be initialized when needed
    
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    
    if 'sensor_data_history' not in st.session_state:
        st.session_state.sensor_data_history = []
    
    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = datetime.now()


def create_parameter_controls() -> SimulationParameters:
    """Create sidebar controls for simulation parameters."""
    st.sidebar.markdown("## 🎛️ Simulation Parameters")
    
    # Mission parameters
    st.sidebar.markdown("### Mission Configuration")
    mission_duration = st.sidebar.slider(
        "Mission Duration (hours)", 
        min_value=0.5, max_value=24.0, value=1.0, step=0.5
    ) * 3600  # Convert to seconds
    
    time_step = st.sidebar.slider(
        "Time Step (seconds)", 
        min_value=0.1, max_value=10.0, value=1.0, step=0.1
    )
    
    # Spacecraft parameters
    st.sidebar.markdown("### Spacecraft Configuration")
    mass = st.sidebar.number_input(
        "Spacecraft Mass (kg)", 
        min_value=100.0, max_value=10000.0, value=1000.0, step=100.0
    )
    
    thrust = st.sidebar.number_input(
        "Maximum Thrust (N)", 
        min_value=1000.0, max_value=50000.0, value=10000.0, step=1000.0
    )
    
    fuel_capacity = st.sidebar.number_input(
        "Fuel Capacity (kg)", 
        min_value=50.0, max_value=2000.0, value=500.0, step=50.0
    )
    
    # Orbital parameters
    st.sidebar.markdown("### Orbital Parameters")
    initial_altitude = st.sidebar.number_input(
        "Initial Altitude (km)", 
        min_value=200.0, max_value=2000.0, value=400.0, step=50.0
    ) * 1000  # Convert to meters
    
    initial_velocity = st.sidebar.number_input(
        "Initial Velocity (m/s)", 
        min_value=7000.0, max_value=9000.0, value=7800.0, step=100.0
    )
    
    return SimulationParameters(
        mission_duration=mission_duration,
        time_step=time_step,
        mass=mass,
        thrust=thrust,
        fuel_capacity=fuel_capacity,
        initial_altitude=initial_altitude,
        initial_velocity=initial_velocity
    )


def create_simulation_controls():
    """Create simulation control buttons."""
    st.markdown("## 🚀 Simulation Controls")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("▶️ Start Simulation", type="primary"):
            st.session_state.simulation_running = True
            st.rerun()
    
    with col2:
        if st.button("⏸️ Pause"):
            st.session_state.simulation_running = False
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset"):
            st.session_state.simulation.reset()
            st.session_state.sensor_generator.reset_sensors()
            st.session_state.sensor_data_history = []
            st.session_state.simulation_running = False
            st.rerun()
    
    with col4:
        if st.button("⏭️ Step Forward"):
            if not st.session_state.simulation_running:
                state = st.session_state.simulation.step()
                if state:
                    sensor_data = st.session_state.sensor_generator.generate_sensor_data(state)
                    st.session_state.sensor_data_history.append(sensor_data)
                st.rerun()
    
    with col5:
        auto_refresh = st.checkbox("Auto Refresh", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh


def display_simulation_status():
    """Display current simulation status and key metrics."""
    if not st.session_state.simulation.current_state:
        st.warning("⚠️ Simulation not initialized. Please reset and start simulation.")
        return
    
    state = st.session_state.simulation.current_state
    stats = st.session_state.simulation.get_simulation_stats()
    
    # Status indicator
    status_class = "status-active" if state.is_active else "status-inactive"
    status_text = "🟢 ACTIVE" if state.is_active else "🔴 INACTIVE"
    
    st.markdown(f"""
    <div class="simulation-status {status_class}">
        <h3>Mission Status: {status_text}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Mission Time",
            value=f"{state.time/3600:.2f} h",
            delta=f"{state.time/60:.1f} min"
        )
        st.metric(
            label="Altitude",
            value=f"{state.altitude/1000:.1f} km",
            delta=f"{(state.altitude - 400000)/1000:.1f} km"
        )
    
    with col2:
        st.metric(
            label="Speed",
            value=f"{state.speed:.0f} m/s",
            delta=f"{state.speed - 7800:.0f} m/s"
        )
        st.metric(
            label="Fuel Remaining",
            value=f"{state.fuel_remaining:.1f} kg",
            delta=f"-{st.session_state.simulation.parameters.fuel_capacity - state.fuel_remaining:.1f} kg"
        )
    
    with col3:
        orbital_elements = stats.get('current_orbital_elements', {})
        period = orbital_elements.get('period', 0)
        if period != float('inf') and period > 0:
            period_hours = period / 3600
            st.metric(
                label="Orbital Period",
                value=f"{period_hours:.2f} h",
                delta=f"{(period_hours - 1.5):.2f} h"
            )
        else:
            st.metric(label="Orbital Period", value="N/A")
        
        st.metric(
            label="Total Distance",
            value=f"{np.linalg.norm(state.position)/1000:.0f} km"
        )
    
    with col4:
        # System health indicators
        sensor_summary = st.session_state.sensor_generator.get_sensor_summary()
        failed_sensors = sum(1 for s in sensor_summary.values() if not s.get('is_functional', True))
        total_sensors = len(sensor_summary)
        
        st.metric(
            label="Sensor Health",
            value=f"{total_sensors - failed_sensors}/{total_sensors}",
            delta=f"{failed_sensors} failed" if failed_sensors > 0 else "All OK"
        )
        
        st.metric(
            label="Data Points",
            value=f"{len(st.session_state.sensor_data_history)}",
            delta=f"+{1 if st.session_state.simulation_running else 0}"
        )


def create_trajectory_plot() -> go.Figure:
    """Create 3D trajectory plot."""
    if not st.session_state.simulation.state_history:
        return go.Figure()
    
    df = st.session_state.simulation.get_trajectory_data()
    
    if df.empty:
        return go.Figure()
    
    # Create 3D trajectory plot
    fig = go.Figure()
    
    # Add Earth as a sphere
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    earth_radius = 6.371e6  # meters
    
    x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
    y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
    z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig.add_trace(go.Surface(
        x=x_earth, y=y_earth, z=z_earth,
        colorscale='Blues',
        opacity=0.6,
        showscale=False,
        name='Earth'
    ))
    
    # Add trajectory
    fig.add_trace(go.Scatter3d(
        x=df['position_x'],
        y=df['position_y'],
        z=df['position_z'],
        mode='lines+markers',
        name='Spacecraft Trajectory',
        line=dict(color='red', width=3),
        marker=dict(size=3)
    ))
    
    # Add current position
    if len(df) > 0:
        current = df.iloc[-1]
        fig.add_trace(go.Scatter3d(
            x=[current['position_x']],
            y=[current['position_y']],
            z=[current['position_z']],
            mode='markers',
            name='Current Position',
            marker=dict(size=10, color='yellow', symbol='diamond')
        ))
    
    fig.update_layout(
        title="3D Spacecraft Trajectory",
        scene=dict(
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            zaxis_title="Z (m)",
            aspectmode='cube'
        ),
        height=600
    )
    
    return fig


def create_telemetry_plots() -> List[go.Figure]:
    """Create telemetry data plots."""
    if not st.session_state.sensor_data_history:
        return []
    
    df = pd.DataFrame(st.session_state.sensor_data_history)
    figures = []
    
    # Time series for key parameters
    time_col = 'simulation_time'
    
    # Plot 1: Altitude and Speed
    fig1 = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Altitude Over Time', 'Speed Over Time'),
        vertical_spacing=0.1
    )
    
    fig1.add_trace(
        go.Scatter(x=df[time_col], y=df['altitude']/1000, name='Altitude (km)'),
        row=1, col=1
    )
    
    fig1.add_trace(
        go.Scatter(x=df[time_col], y=df['accelerometer_x'], name='Speed (m/s)', line=dict(color='orange')),
        row=2, col=1
    )
    
    fig1.update_layout(height=400, title_text="Flight Parameters")
    figures.append(fig1)
    
    # Plot 2: Power Systems
    fig2 = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Battery Voltage', 'Power Consumption'),
        vertical_spacing=0.1
    )
    
    fig2.add_trace(
        go.Scatter(x=df[time_col], y=df['battery_voltage'], name='Battery (V)', line=dict(color='green')),
        row=1, col=1
    )
    
    fig2.add_trace(
        go.Scatter(x=df[time_col], y=df['power_consumption'], name='Power (W)', line=dict(color='red')),
        row=2, col=1
    )
    
    fig2.update_layout(height=400, title_text="Power Systems")
    figures.append(fig2)
    
    # Plot 3: Environmental Data
    fig3 = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Temperature Sensors', 'Radiation Level'),
        vertical_spacing=0.1
    )
    
    fig3.add_trace(
        go.Scatter(x=df[time_col], y=df['temperature_internal'], name='Internal Temp (°C)', line=dict(color='blue')),
        row=1, col=1
    )
    
    fig3.add_trace(
        go.Scatter(x=df[time_col], y=df['temperature_external'], name='External Temp (°C)', line=dict(color='cyan')),
        row=1, col=1
    )
    
    fig3.add_trace(
        go.Scatter(x=df[time_col], y=df['radiation_level'], name='Radiation (mSv/h)', line=dict(color='purple')),
        row=2, col=1
    )
    
    fig3.update_layout(height=400, title_text="Environmental Sensors")
    figures.append(fig3)
    
    return figures


def create_rag_interface():
    """Create RAG chat interface."""
    st.markdown("## 🤖 Mission Assistant (RAG)")
    
    # Initialize RAG system if not already done
    if st.session_state.rag_system is None:
        with st.spinner("Initializing RAG system..."):
            try:
                st.session_state.rag_system = SpaceMissionRAG()
                st.success("RAG system initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize RAG system: {str(e)}")
                return
    
    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about the mission, sensors, or space flight..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Add current simulation context to the query
                    if st.session_state.simulation.current_state:
                        state = st.session_state.simulation.current_state
                        context = f"""
                        Current mission status:
                        - Time: {state.time/3600:.2f} hours
                        - Altitude: {state.altitude/1000:.1f} km
                        - Speed: {state.speed:.0f} m/s
                        - Fuel: {state.fuel_remaining:.1f} kg
                        - Status: {'Active' if state.is_active else 'Inactive'}
                        
                        User question: {prompt}
                        """
                    else:
                        context = prompt
                    
                    response = st.session_state.rag_system.query(context)
                    st.write(response)
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})


def run_simulation_step():
    """Run a single simulation step if simulation is running."""
    if st.session_state.simulation_running and st.session_state.simulation.current_state:
        if st.session_state.simulation.current_state.is_active:
            # Step simulation
            state = st.session_state.simulation.step()
            
            if state:
                # Generate sensor data
                sensor_data = st.session_state.sensor_generator.generate_sensor_data(state)
                st.session_state.sensor_data_history.append(sensor_data)
                
                # Update last update time
                st.session_state.last_update_time = datetime.now()
        else:
            # Mission completed or failed
            st.session_state.simulation_running = False


def main():
    """Main Streamlit application."""
    
    # Initialize session state
    initialize_session_state()
    
    # App header
    st.title("🚀 Netra - Space Flight Simulation & RAG Platform")
    st.markdown("Real-time space mission simulation with AI-powered mission assistance")
    
    # Sidebar for parameters
    parameters = create_parameter_controls()
    
    # Apply parameter changes
    if st.sidebar.button("Apply Parameter Changes"):
        # Update simulation parameters
        st.session_state.simulation.parameters = parameters
        st.session_state.sensor_generator.parameters = parameters
        st.sidebar.success("Parameters updated!")
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        time.sleep(1)  # 1 second refresh rate
        run_simulation_step()
        st.rerun()
    
    # Manual simulation step when running
    if st.session_state.simulation_running:
        run_simulation_step()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎮 Simulation", "📊 Telemetry", "🗺️ Trajectory", "🤖 Mission Assistant"])
    
    with tab1:
        # Simulation controls
        create_simulation_controls()
        
        # Status display
        display_simulation_status()
        
        # Real-time data table
        if st.session_state.sensor_data_history:
            st.markdown("## 📡 Latest Sensor Readings")
            latest_data = st.session_state.sensor_data_history[-1]
            
            # Create a clean display of latest sensor data
            sensor_cols = st.columns(3)
            with sensor_cols[0]:
                st.markdown("### Navigation")
                st.write(f"Altitude: {latest_data.get('altitude', 0)/1000:.1f} km")
                st.write(f"Latitude: {latest_data.get('gps_latitude', 0):.6f}°")
                st.write(f"Longitude: {latest_data.get('gps_longitude', 0):.6f}°")
            
            with sensor_cols[1]:
                st.markdown("### Power Systems")
                st.write(f"Battery: {latest_data.get('battery_voltage', 0):.1f} V")
                st.write(f"Solar: {latest_data.get('solar_panel_current', 0):.1f} A")
                st.write(f"Power: {latest_data.get('power_consumption', 0):.0f} W")
            
            with sensor_cols[2]:
                st.markdown("### Environment")
                st.write(f"Int. Temp: {latest_data.get('temperature_internal', 0):.1f}°C")
                st.write(f"Ext. Temp: {latest_data.get('temperature_external', 0):.1f}°C")
                st.write(f"Radiation: {latest_data.get('radiation_level', 0):.3f} mSv/h")
    
    with tab2:
        # Telemetry plots
        st.markdown("## 📊 Real-time Telemetry")
        
        if st.session_state.sensor_data_history:
            plots = create_telemetry_plots()
            for plot in plots:
                st.plotly_chart(plot, use_container_width=True)
        else:
            st.info("No telemetry data available. Start the simulation to see real-time data.")
    
    with tab3:
        # 3D trajectory visualization
        st.markdown("## 🗺️ Spacecraft Trajectory")
        
        trajectory_fig = create_trajectory_plot()
        if trajectory_fig.data:
            st.plotly_chart(trajectory_fig, use_container_width=True)
        else:
            st.info("No trajectory data available. Start the simulation to see spacecraft movement.")
    
    with tab4:
        # RAG interface
        create_rag_interface()
    
    # Footer with system info
    st.markdown("---")
    st.markdown(f"**Last Update:** {st.session_state.last_update_time.strftime('%H:%M:%S')}")
    
    # Auto-refresh button
    if st.button("🔄 Force Refresh"):
        st.rerun()


if __name__ == "__main__":
    main()
