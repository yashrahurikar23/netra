"""
Synthetic sensor data generation for space flight simulation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

from .simulation import SimulationState, SimulationParameters

logger = logging.getLogger(__name__)


@dataclass
class SensorConfig:
    """Configuration for a sensor type."""
    
    name: str
    unit: str
    base_noise_level: float = 0.01  # 1% noise
    drift_rate: float = 0.001  # per time step
    failure_probability: float = 0.0001  # per time step
    measurement_range: Tuple[float, float] = (0.0, 1000.0)
    precision: int = 3  # decimal places
    sampling_rate: float = 1.0  # Hz


class SensorDataGenerator:
    """
    Generate realistic synthetic sensor data for space missions.
    
    Features:
    - Multiple sensor types (accelerometer, gyroscope, temperature, etc.)
    - Configurable noise and drift
    - Sensor failure simulation
    - Time-series data generation
    - Real-time data streaming capability
    """
    
    def __init__(self, parameters: Optional[SimulationParameters] = None):
        self.parameters = parameters or SimulationParameters()
        self.sensor_configs = self._initialize_sensor_configs()
        self.sensor_states = self._initialize_sensor_states()
        self.data_history: List[Dict[str, Any]] = []
        
    def _initialize_sensor_configs(self) -> Dict[str, SensorConfig]:
        """Initialize standard space mission sensor configurations."""
        return {
            # Inertial Measurement Unit (IMU)
            'accelerometer_x': SensorConfig(
                name='Accelerometer X', unit='m/s²', 
                base_noise_level=0.005, measurement_range=(-100, 100)
            ),
            'accelerometer_y': SensorConfig(
                name='Accelerometer Y', unit='m/s²', 
                base_noise_level=0.005, measurement_range=(-100, 100)
            ),
            'accelerometer_z': SensorConfig(
                name='Accelerometer Z', unit='m/s²', 
                base_noise_level=0.005, measurement_range=(-100, 100)
            ),
            'gyroscope_x': SensorConfig(
                name='Gyroscope X', unit='rad/s', 
                base_noise_level=0.001, measurement_range=(-10, 10)
            ),
            'gyroscope_y': SensorConfig(
                name='Gyroscope Y', unit='rad/s', 
                base_noise_level=0.001, measurement_range=(-10, 10)
            ),
            'gyroscope_z': SensorConfig(
                name='Gyroscope Z', unit='rad/s', 
                base_noise_level=0.001, measurement_range=(-10, 10)
            ),
            
            # Position and Navigation
            'gps_latitude': SensorConfig(
                name='GPS Latitude', unit='degrees', 
                base_noise_level=0.00001, measurement_range=(-90, 90), precision=6
            ),
            'gps_longitude': SensorConfig(
                name='GPS Longitude', unit='degrees', 
                base_noise_level=0.00001, measurement_range=(-180, 180), precision=6
            ),
            'altitude': SensorConfig(
                name='Altitude', unit='meters', 
                base_noise_level=0.01, measurement_range=(100000, 1000000)
            ),
            
            # Environmental Sensors
            'temperature_internal': SensorConfig(
                name='Internal Temperature', unit='°C', 
                base_noise_level=0.1, measurement_range=(-50, 50)
            ),
            'temperature_external': SensorConfig(
                name='External Temperature', unit='°C', 
                base_noise_level=0.5, measurement_range=(-273, 200)
            ),
            'pressure_cabin': SensorConfig(
                name='Cabin Pressure', unit='Pa', 
                base_noise_level=0.001, measurement_range=(50000, 110000)
            ),
            'radiation_level': SensorConfig(
                name='Radiation Level', unit='mSv/h', 
                base_noise_level=0.05, measurement_range=(0, 10)
            ),
            
            # Power Systems
            'battery_voltage': SensorConfig(
                name='Battery Voltage', unit='V', 
                base_noise_level=0.01, measurement_range=(20, 30)
            ),
            'solar_panel_current': SensorConfig(
                name='Solar Panel Current', unit='A', 
                base_noise_level=0.02, measurement_range=(0, 50)
            ),
            'power_consumption': SensorConfig(
                name='Power Consumption', unit='W', 
                base_noise_level=0.01, measurement_range=(100, 2000)
            ),
            
            # Propulsion
            'fuel_level': SensorConfig(
                name='Fuel Level', unit='kg', 
                base_noise_level=0.01, measurement_range=(0, 500)
            ),
            'thrust_magnitude': SensorConfig(
                name='Thrust Magnitude', unit='N', 
                base_noise_level=0.02, measurement_range=(0, 10000)
            ),
            'engine_temperature': SensorConfig(
                name='Engine Temperature', unit='°C', 
                base_noise_level=0.5, measurement_range=(0, 1000)
            ),
            
            # Communication
            'signal_strength': SensorConfig(
                name='Signal Strength', unit='dBm', 
                base_noise_level=0.1, measurement_range=(-120, -30)
            ),
            'data_rate': SensorConfig(
                name='Data Rate', unit='Mbps', 
                base_noise_level=0.05, measurement_range=(0, 100)
            ),
        }
    
    def _initialize_sensor_states(self) -> Dict[str, Dict[str, Any]]:
        """Initialize internal state tracking for each sensor."""
        states = {}
        for sensor_id, config in self.sensor_configs.items():
            states[sensor_id] = {
                'drift_offset': 0.0,
                'is_functional': True,
                'last_measurement': 0.0,
                'calibration_factor': 1.0 + np.random.normal(0, 0.01),  # ±1% calibration error
                'failure_countdown': np.random.exponential(1.0 / config.failure_probability) if config.failure_probability > 0 else float('inf')
            }
        return states
    
    def _calculate_true_value(self, sensor_id: str, sim_state: SimulationState) -> float:
        """Calculate the true physical value for a sensor based on simulation state."""
        if sensor_id == 'accelerometer_x':
            return sim_state.acceleration[0]
        elif sensor_id == 'accelerometer_y':
            return sim_state.acceleration[1]
        elif sensor_id == 'accelerometer_z':
            return sim_state.acceleration[2]
        elif sensor_id in ['gyroscope_x', 'gyroscope_y', 'gyroscope_z']:
            # Simplified: assume small angular velocity for stable orbit
            return np.random.normal(0, 0.001)
        elif sensor_id == 'altitude':
            return sim_state.altitude
        elif sensor_id == 'gps_latitude':
            # Simplified: latitude based on position
            return np.degrees(np.arcsin(sim_state.position[2] / np.linalg.norm(sim_state.position)))
        elif sensor_id == 'gps_longitude':
            # Simplified: longitude based on position
            return np.degrees(np.arctan2(sim_state.position[1], sim_state.position[0]))
        elif sensor_id == 'temperature_internal':
            # Temperature varies with power consumption and external temp
            base_temp = 20.0  # °C
            heat_from_systems = 0.01  # Simple model
            return base_temp + heat_from_systems * sim_state.time
        elif sensor_id == 'temperature_external':
            # Space temperature (very cold)
            return -200.0 + np.random.normal(0, 10)
        elif sensor_id == 'pressure_cabin':
            # Assume pressurized cabin
            return 101325.0  # Standard atmospheric pressure
        elif sensor_id == 'radiation_level':
            # Radiation increases with altitude
            base_radiation = 0.1
            altitude_factor = sim_state.altitude / 400000.0  # Normalized to 400km
            return base_radiation * (1 + altitude_factor)
        elif sensor_id == 'battery_voltage':
            # Battery voltage decreases with time and power consumption
            nominal_voltage = 28.0
            discharge_rate = 0.00001  # Very slow discharge
            return nominal_voltage - discharge_rate * sim_state.time
        elif sensor_id == 'solar_panel_current':
            # Solar panel current varies with orientation (simplified)
            max_current = 40.0
            efficiency = 0.8 + 0.2 * np.sin(sim_state.time / 1000)  # Orbital variation
            return max_current * efficiency
        elif sensor_id == 'power_consumption':
            # Power consumption varies with systems load
            base_power = 1200.0
            variable_power = 200.0 * np.sin(sim_state.time / 500)
            return base_power + variable_power
        elif sensor_id == 'fuel_level':
            return sim_state.fuel_remaining
        elif sensor_id == 'thrust_magnitude':
            # Would be provided by simulation thrust commands
            return 0.0  # Simplified: no thrust unless commanded
        elif sensor_id == 'engine_temperature':
            # Engine temperature correlates with thrust
            return 25.0  # Room temperature when not firing
        elif sensor_id == 'signal_strength':
            # Signal strength varies with distance from ground stations
            base_signal = -80.0  # dBm
            distance_factor = (sim_state.altitude / 400000.0) * 20  # Signal weakens with altitude
            return base_signal - distance_factor
        elif sensor_id == 'data_rate':
            # Data rate correlates with signal strength
            signal_strength = self._calculate_true_value('signal_strength', sim_state)
            max_rate = 50.0
            signal_factor = max(0, (signal_strength + 120) / 90)  # Normalize -120 to -30 dBm
            return max_rate * signal_factor
        else:
            # Default: return a reasonable value
            config = self.sensor_configs[sensor_id]
            return (config.measurement_range[0] + config.measurement_range[1]) / 2
    
    def _apply_sensor_effects(self, sensor_id: str, true_value: float, time_step: float) -> Tuple[float, bool]:
        """Apply noise, drift, and failures to get realistic sensor reading."""
        config = self.sensor_configs[sensor_id]
        state = self.sensor_states[sensor_id]
        
        # Check for sensor failure
        state['failure_countdown'] -= time_step
        if state['failure_countdown'] <= 0:
            state['is_functional'] = False
            logger.warning(f"Sensor {sensor_id} has failed at time {time_step}")
        
        if not state['is_functional']:
            # Return last known value with increasing uncertainty
            uncertainty = min(abs(true_value) * 0.1, 100.0)  # Cap uncertainty
            return state['last_measurement'] + np.random.normal(0, uncertainty), False
        
        # Apply calibration error
        value = true_value * state['calibration_factor']
        
        # Apply drift
        drift_change = np.random.normal(0, config.drift_rate)
        state['drift_offset'] += drift_change
        value += state['drift_offset']
        
        # Apply noise
        noise_std = abs(value) * config.base_noise_level
        value += np.random.normal(0, noise_std)
        
        # Clamp to measurement range
        value = np.clip(value, config.measurement_range[0], config.measurement_range[1])
        
        # Round to precision
        value = round(value, config.precision)
        
        # Update state
        state['last_measurement'] = value
        
        return value, True
    
    def generate_sensor_data(self, sim_state: SimulationState) -> Dict[str, Any]:
        """Generate sensor readings for a single simulation state."""
        timestamp = datetime.now() + timedelta(seconds=sim_state.time)
        
        sensor_data = {
            'timestamp': timestamp,
            'simulation_time': sim_state.time,
            'mission_elapsed_time': sim_state.time,
        }
        
        # Generate readings for each sensor
        for sensor_id, config in self.sensor_configs.items():
            true_value = self._calculate_true_value(sensor_id, sim_state)
            measured_value, is_functional = self._apply_sensor_effects(
                sensor_id, true_value, self.parameters.time_step
            )
            
            sensor_data[sensor_id] = measured_value
            sensor_data[f"{sensor_id}_status"] = "OK" if is_functional else "FAILED"
            sensor_data[f"{sensor_id}_true"] = true_value  # For validation/debugging
        
        self.data_history.append(sensor_data)
        return sensor_data
    
    def generate_batch_data(self, sim_states: List[SimulationState]) -> pd.DataFrame:
        """Generate sensor data for a batch of simulation states."""
        batch_data = []
        
        for state in sim_states:
            sensor_reading = self.generate_sensor_data(state)
            batch_data.append(sensor_reading)
        
        return pd.DataFrame(batch_data)
    
    def get_sensor_summary(self) -> Dict[str, Any]:
        """Get summary statistics for all sensors."""
        if not self.data_history:
            return {}
        
        df = pd.DataFrame(self.data_history)
        summary = {}
        
        for sensor_id, config in self.sensor_configs.items():
            if sensor_id in df.columns:
                sensor_summary = {
                    'name': config.name,
                    'unit': config.unit,
                    'count': len(df[sensor_id]),
                    'mean': df[sensor_id].mean(),
                    'std': df[sensor_id].std(),
                    'min': df[sensor_id].min(),
                    'max': df[sensor_id].max(),
                    'last_value': df[sensor_id].iloc[-1] if len(df) > 0 else None,
                    'is_functional': self.sensor_states[sensor_id]['is_functional'],
                    'drift_offset': self.sensor_states[sensor_id]['drift_offset']
                }
                summary[sensor_id] = sensor_summary
        
        return summary
    
    def reset_sensors(self):
        """Reset all sensors to initial state."""
        self.sensor_states = self._initialize_sensor_states()
        self.data_history = []
        logger.info("All sensors reset to initial state")
    
    def simulate_sensor_failure(self, sensor_id: str):
        """Manually trigger a sensor failure for testing."""
        if sensor_id in self.sensor_states:
            self.sensor_states[sensor_id]['is_functional'] = False
            logger.info(f"Manually triggered failure for sensor {sensor_id}")
    
    def repair_sensor(self, sensor_id: str):
        """Repair a failed sensor."""
        if sensor_id in self.sensor_states:
            self.sensor_states[sensor_id]['is_functional'] = True
            self.sensor_states[sensor_id]['drift_offset'] = 0.0
            # Reset failure countdown
            config = self.sensor_configs[sensor_id]
            self.sensor_states[sensor_id]['failure_countdown'] = (
                np.random.exponential(1.0 / config.failure_probability) 
                if config.failure_probability > 0 else float('inf')
            )
            logger.info(f"Repaired sensor {sensor_id}")
    
    def export_data(self, filepath: str, format: str = 'csv'):
        """Export sensor data to file."""
        if not self.data_history:
            logger.warning("No data to export")
            return
        
        df = pd.DataFrame(self.data_history)
        
        if format.lower() == 'csv':
            df.to_csv(filepath, index=False)
        elif format.lower() == 'json':
            df.to_json(filepath, orient='records', date_format='iso')
        elif format.lower() == 'parquet':
            df.to_parquet(filepath, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        logger.info(f"Exported {len(df)} sensor readings to {filepath}")
