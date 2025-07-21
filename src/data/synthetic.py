"""
Synthetic data generator for testing and development.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


class SyntheticDataGenerator:
    """
    Generate synthetic mission data for testing and development.
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            np.random.seed(seed)
        
        self.missions = [
            "Apollo 11", "Apollo 12", "Apollo 13", "Apollo 14", "Apollo 15",
            "Apollo 16", "Apollo 17", "Voyager 1", "Voyager 2", "Cassini",
            "Galileo", "New Horizons", "Curiosity", "Perseverance", "Ingenuity"
        ]
        
        self.sensor_types = [
            "temperature", "pressure", "radiation", "acceleration", "gyroscope",
            "gps", "altitude", "fuel_level", "battery", "solar_panel"
        ]
    
    def generate_mission_timeline(self, mission_name: str, duration_hours: int = 24) -> List[Dict[str, Any]]:
        """Generate a realistic mission timeline."""
        start_time = datetime.now()
        events = []
        
        # Mission phases
        phases = [
            {"name": "Launch", "duration": 0.25, "events": ["Launch sequence initiated", "Liftoff", "Stage separation"]},
            {"name": "Ascent", "duration": 0.5, "events": ["First stage burnout", "Fairing separation", "Second stage ignition"]},
            {"name": "Orbit Insertion", "duration": 1.0, "events": ["Orbital insertion burn", "Solar panels deployed", "Initial telemetry"]},
            {"name": "Science Operations", "duration": duration_hours - 2, "events": ["Science instruments activated", "Data collection", "Periodic maneuvers"]},
            {"name": "Mission End", "duration": 0.25, "events": ["Final data transmission", "Deorbit preparation", "Mission complete"]}
        ]
        
        current_time = start_time
        
        for phase in phases:
            phase_start = current_time
            phase_duration = timedelta(hours=phase["duration"])
            
            # Add phase start event
            events.append({
                "timestamp": current_time,
                "phase": phase["name"],
                "event": f"{phase['name']} phase started",
                "type": "phase_start"
            })
            
            # Add events within the phase
            for i, event in enumerate(phase["events"]):
                event_time = phase_start + timedelta(hours=phase["duration"] * (i + 1) / len(phase["events"]))
                events.append({
                    "timestamp": event_time,
                    "phase": phase["name"],
                    "event": event,
                    "type": "event"
                })
            
            current_time += phase_duration
        
        return events
    
    def generate_sensor_data(self, mission_name: str, duration_hours: int = 24, sample_rate: int = 60) -> pd.DataFrame:
        """Generate synthetic sensor data for a mission."""
        # Calculate number of samples
        num_samples = duration_hours * 3600 // sample_rate
        
        # Generate time series
        start_time = datetime.now()
        timestamps = [start_time + timedelta(seconds=i * sample_rate) for i in range(num_samples)]
        
        # Generate sensor data
        data = {"timestamp": timestamps}
        
        # Altitude (decreasing slowly due to atmospheric drag)
        base_altitude = 400000  # 400 km
        altitude_decay = np.linspace(0, 1000, num_samples)  # 1 km decay over mission
        altitude_noise = np.random.normal(0, 50, num_samples)
        data["altitude"] = base_altitude - altitude_decay + altitude_noise
        
        # Temperature (internal)
        base_temp = 20  # °C
        temp_variation = 5 * np.sin(2 * np.pi * np.arange(num_samples) / (3600 / sample_rate))  # 1-hour cycle
        temp_noise = np.random.normal(0, 0.5, num_samples)
        data["temperature_internal"] = base_temp + temp_variation + temp_noise
        
        # Battery voltage (decreasing with usage)
        base_voltage = 28.0  # V
        voltage_drain = np.linspace(0, 3, num_samples)  # 3V drain over mission
        voltage_noise = np.random.normal(0, 0.1, num_samples)
        data["battery_voltage"] = base_voltage - voltage_drain + voltage_noise
        
        # Solar panel current (varies with orbit)
        max_current = 40  # A
        orbital_period = 90 * 60  # 90 minutes in seconds
        orbital_variation = 0.5 * (1 + np.sin(2 * np.pi * np.arange(num_samples) * sample_rate / orbital_period))
        current_noise = np.random.normal(0, 1, num_samples)
        data["solar_panel_current"] = max_current * orbital_variation + current_noise
        
        # Fuel level (decreasing with maneuvers)
        initial_fuel = 500  # kg
        fuel_consumption = np.cumsum(np.random.exponential(0.1, num_samples))
        data["fuel_level"] = np.maximum(0, initial_fuel - fuel_consumption)
        
        # Acceleration (mostly gravity + small perturbations)
        gravity = 9.81  # m/s²
        accel_noise = np.random.normal(0, 0.1, num_samples)
        data["acceleration_x"] = accel_noise
        data["acceleration_y"] = accel_noise
        data["acceleration_z"] = -gravity + accel_noise
        
        # Pressure (cabin pressure, should be stable)
        cabin_pressure = 101325  # Pa
        pressure_noise = np.random.normal(0, 100, num_samples)
        data["pressure_cabin"] = cabin_pressure + pressure_noise
        
        # Radiation (varies with altitude and orbit)
        base_radiation = 0.1  # mSv/h
        radiation_variation = 0.05 * np.sin(2 * np.pi * np.arange(num_samples) / 1000)  # Slow variation
        radiation_noise = np.random.normal(0, 0.01, num_samples)
        data["radiation_level"] = base_radiation + radiation_variation + radiation_noise
        
        return pd.DataFrame(data)
    
    def generate_mission_report(self, mission_name: str, success: bool = True) -> str:
        """Generate a synthetic mission report."""
        status = "SUCCESS" if success else "PARTIAL SUCCESS"
        
        report = f"""# Mission Report: {mission_name}

## Mission Status: {status}

### Executive Summary
The {mission_name} mission has been completed with {status.lower()} status. 
All primary objectives were {"achieved" if success else "partially achieved"}.

### Mission Timeline
- Launch: Successful
- Orbit Insertion: Nominal
- Science Operations: {"Completed" if success else "Partially completed"}
- Mission End: Controlled

### Technical Performance
- Altitude Control: ±50 m accuracy maintained
- Power Systems: Operated within specifications
- Communication: 99.5% uptime
- Sensor Performance: All sensors operational

### Anomalies
{"None reported" if success else "Minor sensor calibration issues resolved"}

### Lessons Learned
- Orbital mechanics simulation performed well
- Sensor data quality exceeded expectations
- RAG system provided valuable mission assistance

### Recommendations
- Continue monitoring atmospheric drag effects
- Implement improved battery management
- Enhance radiation monitoring capabilities

### Data Summary
- Total mission duration: 24 hours
- Data points collected: 86,400
- Sensor readings: 100% valid
- Mission success rate: {"100%" if success else "95%"}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def generate_anomaly_data(self, num_anomalies: int = 10) -> List[Dict[str, Any]]:
        """Generate synthetic anomaly data."""
        anomaly_types = [
            "Sensor drift", "Communication loss", "Power fluctuation", 
            "Attitude control issue", "Thermal anomaly", "Fuel leak",
            "Solar panel degradation", "Computer glitch", "Orbital decay"
        ]
        
        severity_levels = ["Low", "Medium", "High", "Critical"]
        
        anomalies = []
        
        for i in range(num_anomalies):
            anomaly = {
                "id": f"ANOM-{i+1:03d}",
                "type": np.random.choice(anomaly_types),
                "severity": np.random.choice(severity_levels),
                "timestamp": datetime.now() + timedelta(minutes=np.random.randint(0, 1440)),
                "description": f"Anomaly detected in {np.random.choice(self.sensor_types)} system",
                "resolution": np.random.choice(["Resolved", "Monitoring", "Workaround", "Pending"]),
                "impact": np.random.choice(["None", "Minor", "Moderate", "Significant"])
            }
            
            anomalies.append(anomaly)
        
        return anomalies
    
    def save_synthetic_data(self, output_dir: str):
        """Save all synthetic data to files."""
        from pathlib import Path
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate data for multiple missions
        for mission in self.missions[:3]:  # Generate data for first 3 missions
            
            # Mission timeline
            timeline = self.generate_mission_timeline(mission)
            timeline_df = pd.DataFrame(timeline)
            timeline_df.to_csv(output_path / f"{mission.replace(' ', '_')}_timeline.csv", index=False)
            
            # Sensor data
            sensor_data = self.generate_sensor_data(mission)
            sensor_data.to_csv(output_path / f"{mission.replace(' ', '_')}_sensors.csv", index=False)
            
            # Mission report
            report = self.generate_mission_report(mission)
            with open(output_path / f"{mission.replace(' ', '_')}_report.md", 'w') as f:
                f.write(report)
        
        # Anomaly data
        anomalies = self.generate_anomaly_data()
        anomaly_df = pd.DataFrame(anomalies)
        anomaly_df.to_csv(output_path / "anomalies.csv", index=False)
        
        logger.info(f"Generated synthetic data in {output_path}")
        
        return {
            "missions": len(self.missions[:3]),
            "files_created": len(list(output_path.glob("*"))),
            "total_data_points": len(sensor_data) * 3
        }
