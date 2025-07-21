"""
Reusable UI components for the Netra platform.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional
import numpy as np


def create_metric_card(title: str, value: str, delta: Optional[str] = None, help_text: Optional[str] = None):
    """Create a styled metric card."""
    delta_html = f"<div style='color: #666; font-size: 0.8em;'>{delta}</div>" if delta else ""
    help_html = f"<div style='color: #999; font-size: 0.7em; margin-top: 0.5em;'>{help_text}</div>" if help_text else ""
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    '>
        <h4 style='margin: 0; color: #495057; font-size: 0.9em;'>{title}</h4>
        <h2 style='margin: 0.25rem 0; color: #212529;'>{value}</h2>
        {delta_html}
        {help_html}
    </div>
    """, unsafe_allow_html=True)


def create_status_indicator(status: str, is_active: bool = True):
    """Create a visual status indicator."""
    color = "#28a745" if is_active else "#dc3545"
    icon = "🟢" if is_active else "🔴"
    
    st.markdown(f"""
    <div style='
        display: flex;
        align-items: center;
        padding: 0.75rem;
        background-color: {"#d4edda" if is_active else "#f8d7da"};
        border: 1px solid {"#c3e6cb" if is_active else "#f5c6cb"};
        border-radius: 0.5rem;
        margin: 1rem 0;
    '>
        <span style='margin-right: 0.5rem; font-size: 1.2em;'>{icon}</span>
        <strong style='color: {color}; font-size: 1.1em;'>{status}</strong>
    </div>
    """, unsafe_allow_html=True)


def create_parameter_group(title: str, parameters: Dict[str, Any], key_prefix: str = ""):
    """Create a collapsible parameter group."""
    with st.expander(f"⚙️ {title}", expanded=False):
        cols = st.columns(2)
        param_values = {}
        
        for i, (param_name, config) in enumerate(parameters.items()):
            col = cols[i % 2]
            
            with col:
                if config['type'] == 'slider':
                    value = st.slider(
                        config['label'],
                        min_value=config['min'],
                        max_value=config['max'],
                        value=config['default'],
                        step=config.get('step', 1),
                        key=f"{key_prefix}_{param_name}"
                    )
                elif config['type'] == 'number':
                    value = st.number_input(
                        config['label'],
                        min_value=config['min'],
                        max_value=config['max'],
                        value=config['default'],
                        step=config.get('step', 1),
                        key=f"{key_prefix}_{param_name}"
                    )
                elif config['type'] == 'select':
                    value = st.selectbox(
                        config['label'],
                        options=config['options'],
                        index=config['options'].index(config['default']),
                        key=f"{key_prefix}_{param_name}"
                    )
                
                param_values[param_name] = value
        
        return param_values


def create_sensor_grid(sensor_data: Dict[str, Any], columns: int = 4):
    """Create a grid layout for sensor readings."""
    sensor_items = list(sensor_data.items())
    
    for i in range(0, len(sensor_items), columns):
        cols = st.columns(columns)
        
        for j, col in enumerate(cols):
            if i + j < len(sensor_items):
                sensor_name, sensor_value = sensor_items[i + j]
                
                # Skip status and true value columns
                if '_status' in sensor_name or '_true' in sensor_name:
                    continue
                
                with col:
                    # Get sensor status
                    status_key = f"{sensor_name}_status"
                    status = sensor_data.get(status_key, "OK")
                    
                    # Color based on status
                    color = "#28a745" if status == "OK" else "#dc3545"
                    
                    st.markdown(f"""
                    <div style='
                        text-align: center;
                        padding: 0.75rem;
                        border: 2px solid {color};
                        border-radius: 8px;
                        margin: 0.25rem;
                        background-color: {"#f8f9fa" if status == "OK" else "#ffe6e6"};
                    '>
                        <div style='font-size: 0.8em; color: #666; font-weight: bold;'>
                            {sensor_name.replace('_', ' ').title()}
                        </div>
                        <div style='font-size: 1.2em; font-weight: bold; color: #212529; margin: 0.25rem 0;'>
                            {sensor_value:.3f if isinstance(sensor_value, (int, float)) else sensor_value}
                        </div>
                        <div style='font-size: 0.7em; color: {color}; font-weight: bold;'>
                            {status}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


def create_3d_earth():
    """Create a 3D Earth representation for trajectory plots."""
    # Create sphere coordinates for Earth
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    earth_radius = 6.371e6  # meters
    
    x = earth_radius * np.outer(np.cos(u), np.sin(v))
    y = earth_radius * np.outer(np.sin(u), np.sin(v))
    z = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    return go.Surface(
        x=x, y=y, z=z,
        colorscale='Earth',
        opacity=0.8,
        showscale=False,
        name='Earth'
    )


def create_alert_banner(message: str, alert_type: str = "info"):
    """Create an alert banner."""
    colors = {
        "info": {"bg": "#d1ecf1", "border": "#bee5eb", "text": "#0c5460"},
        "success": {"bg": "#d4edda", "border": "#c3e6cb", "text": "#155724"},
        "warning": {"bg": "#fff3cd", "border": "#ffeaa7", "text": "#856404"},
        "error": {"bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24"}
    }
    
    color = colors.get(alert_type, colors["info"])
    
    st.markdown(f"""
    <div style='
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid {color["border"]};
        border-radius: 0.5rem;
        background-color: {color["bg"]};
        color: {color["text"]};
    '>
        {message}
    </div>
    """, unsafe_allow_html=True)


def create_progress_ring(value: float, max_value: float, label: str, color: str = "#007bff"):
    """Create a circular progress indicator."""
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    
    st.markdown(f"""
    <div style='text-align: center; margin: 1rem;'>
        <div style='
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: conic-gradient({color} {percentage * 3.6}deg, #e9ecef 0deg);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.5rem;
        '>
            <div style='
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: {color};
            '>
                {percentage:.0f}%
            </div>
        </div>
        <div style='font-size: 0.9em; color: #666;'>{label}</div>
        <div style='font-size: 0.8em; color: #999;'>{value:.1f} / {max_value:.1f}</div>
    </div>
    """, unsafe_allow_html=True)


def create_timeline_event(timestamp: str, event: str, event_type: str = "info"):
    """Create a timeline event entry."""
    colors = {
        "info": "#007bff",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545"
    }
    
    color = colors.get(event_type, colors["info"])
    
    st.markdown(f"""
    <div style='
        display: flex;
        margin: 0.5rem 0;
        padding: 0.75rem;
        border-left: 4px solid {color};
        background-color: #f8f9fa;
        border-radius: 0 8px 8px 0;
    '>
        <div style='
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: {color};
            margin-right: 1rem;
            margin-top: 0.25rem;
            flex-shrink: 0;
        '></div>
        <div style='flex-grow: 1;'>
            <div style='font-size: 0.8em; color: #666; margin-bottom: 0.25rem;'>{timestamp}</div>
            <div style='color: #212529;'>{event}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
