"""
Space flight simulation with real-time parameter control.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional, List, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class SimulationParameters:
    """Parameters controlling the space flight simulation."""
    
    # Mission parameters
    mission_duration: float = 3600.0  # seconds
    time_step: float = 1.0  # seconds
    
    # Spacecraft parameters
    mass: float = 1000.0  # kg
    thrust: float = 10000.0  # N
    fuel_capacity: float = 500.0  # kg
    fuel_consumption_rate: float = 0.1  # kg/s
    
    # Orbit parameters
    initial_altitude: float = 400000.0  # meters above Earth
    initial_velocity: float = 7800.0  # m/s
    orbital_inclination: float = 0.0  # degrees
    
    # Environmental parameters
    atmospheric_density: float = 1e-12  # kg/m³ (very thin at 400km)
    drag_coefficient: float = 2.2
    spacecraft_area: float = 10.0  # m²
    
    # Sensor parameters
    sensor_noise_level: float = 0.01  # 1% noise
    sensor_failure_rate: float = 0.001  # 0.1% chance per time step


@dataclass
class SimulationState:
    """Current state of the spacecraft simulation."""
    
    time: float
    position: np.ndarray  # [x, y, z] in meters
    velocity: np.ndarray  # [vx, vy, vz] in m/s
    acceleration: np.ndarray  # [ax, ay, az] in m/s²
    fuel_remaining: float  # kg
    altitude: float  # meters above Earth
    speed: float  # m/s
    is_active: bool = True
    
    def to_dict(self) -> Dict:
        """Convert state to dictionary for storage/transmission."""
        return {
            'time': self.time,
            'position_x': self.position[0],
            'position_y': self.position[1],
            'position_z': self.position[2],
            'velocity_x': self.velocity[0],
            'velocity_y': self.velocity[1],
            'velocity_z': self.velocity[2],
            'acceleration_x': self.acceleration[0],
            'acceleration_y': self.acceleration[1],
            'acceleration_z': self.acceleration[2],
            'fuel_remaining': self.fuel_remaining,
            'altitude': self.altitude,
            'speed': self.speed,
            'is_active': self.is_active
        }


class SpaceFlightSimulation:
    """
    Real-time space flight simulation with configurable parameters.
    
    Features:
    - Orbital mechanics simulation
    - Real-time parameter adjustment
    - Atmospheric drag and gravitational effects
    - Fuel consumption modeling
    - State history tracking
    """
    
    # Earth constants
    EARTH_RADIUS = 6.371e6  # meters
    EARTH_MASS = 5.972e24  # kg
    GRAVITATIONAL_CONSTANT = 6.674e-11  # m³/kg/s²
    
    def __init__(self, parameters: Optional[SimulationParameters] = None):
        self.parameters = parameters or SimulationParameters()
        self.current_state: Optional[SimulationState] = None
        self.state_history: List[SimulationState] = []
        self.start_time = datetime.now()
        self.is_running = False
        
        # Initialize simulation state
        self.reset()
    
    def reset(self):
        """Reset simulation to initial conditions."""
        # Initial position: circular orbit at specified altitude
        initial_radius = self.EARTH_RADIUS + self.parameters.initial_altitude
        
        # Start at (radius, 0, 0) for simplicity
        position = np.array([initial_radius, 0.0, 0.0])
        
        # Initial velocity: circular orbit velocity in y-direction
        orbital_velocity = np.sqrt(
            self.GRAVITATIONAL_CONSTANT * self.EARTH_MASS / initial_radius
        )
        velocity = np.array([0.0, orbital_velocity, 0.0])
        
        self.current_state = SimulationState(
            time=0.0,
            position=position,
            velocity=velocity,
            acceleration=np.zeros(3),
            fuel_remaining=self.parameters.fuel_capacity,
            altitude=self.parameters.initial_altitude,
            speed=orbital_velocity,
            is_active=True
        )
        
        self.state_history = [self.current_state]
        self.is_running = False
        
        logger.info(f"Simulation reset. Initial altitude: {self.parameters.initial_altitude/1000:.1f} km")
    
    def calculate_gravitational_force(self, position: np.ndarray) -> np.ndarray:
        """Calculate gravitational force on spacecraft."""
        r_magnitude = np.linalg.norm(position)
        if r_magnitude == 0:
            return np.zeros(3)
        
        # Newton's law of universal gravitation
        force_magnitude = (
            self.GRAVITATIONAL_CONSTANT * self.EARTH_MASS * self.parameters.mass
            / (r_magnitude ** 2)
        )
        
        # Force direction: toward Earth center
        force_direction = -position / r_magnitude
        
        return force_magnitude * force_direction
    
    def calculate_atmospheric_drag(self, velocity: np.ndarray, altitude: float) -> np.ndarray:
        """Calculate atmospheric drag force."""
        if altitude > 600000:  # Above 600km, negligible atmosphere
            return np.zeros(3)
        
        # Simple atmospheric model: exponential decay
        scale_height = 8000  # meters
        density = self.parameters.atmospheric_density * np.exp(-altitude / scale_height)
        
        speed = np.linalg.norm(velocity)
        if speed == 0:
            return np.zeros(3)
        
        # Drag force: F = 0.5 * ρ * v² * Cd * A
        drag_magnitude = (
            0.5 * density * speed**2 * 
            self.parameters.drag_coefficient * self.parameters.spacecraft_area
        )
        
        # Drag direction: opposite to velocity
        drag_direction = -velocity / speed
        
        return drag_magnitude * drag_direction
    
    def calculate_thrust_force(self, thrust_vector: np.ndarray) -> Tuple[np.ndarray, float]:
        """Calculate thrust force and fuel consumption."""
        if not self.current_state or self.current_state.fuel_remaining <= 0:
            return np.zeros(3), 0.0
        
        thrust_magnitude = np.linalg.norm(thrust_vector)
        if thrust_magnitude == 0:
            return np.zeros(3), 0.0
        
        # Limit thrust to available capacity
        max_thrust = min(thrust_magnitude, self.parameters.thrust)
        
        # Calculate fuel consumption
        fuel_consumed = (
            self.parameters.fuel_consumption_rate * 
            (max_thrust / self.parameters.thrust) * 
            self.parameters.time_step
        )
        
        # Normalize thrust vector
        thrust_direction = thrust_vector / thrust_magnitude
        
        return max_thrust * thrust_direction, fuel_consumed
    
    def step(self, thrust_vector: Optional[np.ndarray] = None) -> Optional[SimulationState]:
        """Advance simulation by one time step."""
        if not self.current_state or not self.current_state.is_active:
            return self.current_state
        
        if thrust_vector is None:
            thrust_vector = np.zeros(3)
        
        # Calculate forces
        gravitational_force = self.calculate_gravitational_force(self.current_state.position)
        drag_force = self.calculate_atmospheric_drag(
            self.current_state.velocity, 
            self.current_state.altitude
        )
        thrust_force, fuel_consumed = self.calculate_thrust_force(thrust_vector)
        
        # Total force and acceleration
        total_force = gravitational_force + drag_force + thrust_force
        acceleration = total_force / self.parameters.mass
        
        # Update state using Euler integration
        new_velocity = self.current_state.velocity + acceleration * self.parameters.time_step
        new_position = self.current_state.position + new_velocity * self.parameters.time_step
        
        # Update fuel
        new_fuel = max(0, self.current_state.fuel_remaining - fuel_consumed)
        
        # Calculate derived quantities
        new_altitude = np.linalg.norm(new_position) - self.EARTH_RADIUS
        new_speed = np.linalg.norm(new_velocity)
        
        # Check if mission is still active
        is_active = (
            new_altitude > 100000 and  # Above 100km (Kármán line)
            new_fuel > 0 and
            self.current_state.time < self.parameters.mission_duration
        )
        
        # Create new state
        new_state = SimulationState(
            time=self.current_state.time + self.parameters.time_step,
            position=new_position,
            velocity=new_velocity,
            acceleration=acceleration,
            fuel_remaining=new_fuel,
            altitude=new_altitude,
            speed=new_speed,
            is_active=is_active
        )
        
        self.current_state = new_state
        self.state_history.append(new_state)
        
        return new_state
    
    def run_simulation(self, steps: Optional[int] = None, thrust_profile: Optional[List[np.ndarray]] = None) -> List[SimulationState]:
        """Run simulation for specified number of steps."""
        if steps is None:
            steps = int(self.parameters.mission_duration / self.parameters.time_step)
        
        if thrust_profile is None:
            thrust_profile = [np.zeros(3)] * steps
        
        self.is_running = True
        
        for i in range(steps):
            if not self.current_state or not self.current_state.is_active:
                break
            
            thrust = thrust_profile[i] if i < len(thrust_profile) else np.zeros(3)
            self.step(thrust)
        
        self.is_running = False
        return self.state_history
    
    def get_trajectory_data(self) -> pd.DataFrame:
        """Get trajectory data as pandas DataFrame."""
        if not self.state_history:
            return pd.DataFrame()
        
        data = []
        for state in self.state_history:
            data.append(state.to_dict())
        
        return pd.DataFrame(data)
    
    def get_current_orbital_elements(self) -> Dict[str, float]:
        """Calculate and return current orbital elements."""
        if not self.current_state:
            return {}
        
        r_vec = self.current_state.position
        v_vec = self.current_state.velocity
        
        r_magnitude = np.linalg.norm(r_vec)
        v_magnitude = np.linalg.norm(v_vec)
        
        # Semi-major axis (simplified for circular orbits)
        mu = self.GRAVITATIONAL_CONSTANT * self.EARTH_MASS
        energy = 0.5 * v_magnitude**2 - mu / r_magnitude
        semi_major_axis = -mu / (2 * energy) if energy < 0 else float('inf')
        
        # Orbital period
        if semi_major_axis > 0 and semi_major_axis != float('inf'):
            period = 2 * np.pi * np.sqrt(semi_major_axis**3 / mu)
        else:
            period = float('inf')
        
        return {
            'altitude': self.current_state.altitude,
            'speed': self.current_state.speed,
            'semi_major_axis': semi_major_axis,
            'period': period,
            'apoapsis': r_magnitude,  # Simplified
            'periapsis': r_magnitude,  # Simplified for circular orbit
        }
    
    def update_parameters(self, new_parameters: Dict[str, float]):
        """Update simulation parameters during runtime."""
        for key, value in new_parameters.items():
            if hasattr(self.parameters, key):
                setattr(self.parameters, key, value)
                logger.info(f"Updated parameter {key} to {value}")
    
    def get_simulation_stats(self) -> Dict[str, Any]:
        """Get comprehensive simulation statistics."""
        if not self.state_history:
            return {}
        
        df = self.get_trajectory_data()
        
        return {
            'total_time': self.current_state.time if self.current_state else 0,
            'total_steps': len(self.state_history),
            'max_altitude': df['altitude'].max() if not df.empty else 0,
            'min_altitude': df['altitude'].min() if not df.empty else 0,
            'max_speed': df['speed'].max() if not df.empty else 0,
            'min_speed': df['speed'].min() if not df.empty else 0,
            'fuel_consumed': self.parameters.fuel_capacity - (
                self.current_state.fuel_remaining if self.current_state else 0
            ),
            'is_active': self.current_state.is_active if self.current_state else False,
            'current_orbital_elements': self.get_current_orbital_elements()
        }
