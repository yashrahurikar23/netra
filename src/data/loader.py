"""
Data loader for mission documents and historical data.
"""

import os
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Load and manage mission documents and historical data for the RAG system.
    """
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.synthetic_dir = self.data_dir / "synthetic"
        
        # Create directories if they don't exist
        for dir_path in [self.raw_dir, self.processed_dir, self.synthetic_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def load_mission_documents(self) -> List[Dict[str, Any]]:
        """Load mission documents from the raw data directory."""
        documents = []
        
        # Look for various document types
        for file_path in self.raw_dir.glob("**/*"):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() in ['.txt', '.md']:
                        # Text documents
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        documents.append({
                            'filename': file_path.name,
                            'path': str(file_path),
                            'type': 'text',
                            'content': content,
                            'metadata': {
                                'file_size': file_path.stat().st_size,
                                'modified': file_path.stat().st_mtime
                            }
                        })
                    
                    elif file_path.suffix.lower() == '.json':
                        # JSON documents
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        documents.append({
                            'filename': file_path.name,
                            'path': str(file_path),
                            'type': 'json',
                            'content': json.dumps(data, indent=2),
                            'data': data,
                            'metadata': {
                                'file_size': file_path.stat().st_size,
                                'modified': file_path.stat().st_mtime
                            }
                        })
                    
                    elif file_path.suffix.lower() in ['.csv']:
                        # CSV documents
                        df = pd.read_csv(file_path)
                        
                        documents.append({
                            'filename': file_path.name,
                            'path': str(file_path),
                            'type': 'csv',
                            'content': df.to_string(),
                            'data': df,
                            'metadata': {
                                'file_size': file_path.stat().st_size,
                                'modified': file_path.stat().st_mtime,
                                'rows': len(df),
                                'columns': len(df.columns)
                            }
                        })
                
                except Exception as e:
                    logger.warning(f"Failed to load {file_path}: {e}")
        
        logger.info(f"Loaded {len(documents)} documents from {self.raw_dir}")
        return documents
    
    def create_sample_mission_data(self):
        """Create sample mission documents for demonstration."""
        sample_docs = {
            'mission_overview.md': """# Mission Overview: Netra Space Flight Simulation

## Mission Objectives
- Demonstrate orbital mechanics simulation
- Test real-time sensor data processing
- Validate AI-powered mission assistance

## Spacecraft Specifications
- Mass: 1000 kg
- Thrust: 10,000 N
- Fuel Capacity: 500 kg
- Initial Orbit: 400 km altitude

## Mission Timeline
- Launch: T+0
- Orbit insertion: T+15 minutes
- Science operations: T+30 minutes
- Mission duration: 1-24 hours

## Success Criteria
- Maintain stable orbit
- Collect continuous sensor data
- Respond to parameter changes
- Provide AI assistance for mission operations
""",
            
            'sensor_specifications.md': """# Sensor Specifications

## Inertial Measurement Unit (IMU)
- Accelerometer: ±100 m/s², 0.5% accuracy
- Gyroscope: ±10 rad/s, 0.1% accuracy
- Sample rate: 100 Hz

## Navigation Systems
- GPS: ±10 m accuracy
- Altitude sensor: ±100 m accuracy
- Attitude determination: ±0.1° accuracy

## Environmental Sensors
- Internal temperature: -50°C to +50°C, ±0.1°C
- External temperature: -273°C to +200°C, ±0.5°C
- Radiation detector: 0-10 mSv/h, ±5% accuracy

## Power Systems
- Battery voltage monitor: 20-30V, ±0.1V
- Solar panel current: 0-50A, ±0.5A
- Power consumption: 100-2000W, ±1%

## Communication
- Signal strength: -120 to -30 dBm
- Data rate: 0-100 Mbps
- Link margin: >10 dB required
""",
            
            'orbital_mechanics.md': """# Orbital Mechanics Reference

## Basic Principles
- Gravitational force: F = GMm/r²
- Orbital velocity: v = √(GM/r)
- Orbital period: T = 2π√(r³/GM)

## Common Orbits
- Low Earth Orbit (LEO): 200-2000 km
- Geostationary Orbit (GEO): 35,786 km
- Sun-synchronous Orbit: 600-800 km

## Perturbations
- Atmospheric drag (below 600 km)
- Solar radiation pressure
- Gravitational anomalies
- Third-body effects (Moon, Sun)

## Maneuvers
- Hohmann transfer
- Bi-elliptic transfer
- Plane change maneuvers
- Orbit circularization

## Simulation Parameters
- Earth radius: 6,371 km
- Earth mass: 5.972 × 10²⁴ kg
- Standard gravity: 9.81 m/s²
- Atmospheric scale height: 8 km
""",
            
            'emergency_procedures.md': """# Emergency Procedures

## Power System Failure
1. Switch to backup power
2. Reduce non-essential systems
3. Prioritize life support and communication
4. Attempt solar panel deployment

## Communication Loss
1. Check antenna orientation
2. Increase transmission power
3. Switch to backup frequency
4. Activate emergency beacon

## Sensor Failures
1. Cross-check with redundant sensors
2. Recalibrate if possible
3. Switch to backup sensors
4. Estimate values from other data

## Attitude Control Issues
1. Check thruster status
2. Use reaction wheels if available
3. Attempt magnetic torquers
4. Prepare for safe mode

## Fuel Depletion
1. Calculate remaining delta-v
2. Prioritize mission objectives
3. Plan deorbit maneuver
4. Activate emergency systems
"""
        }
        
        # Create sample documents
        for filename, content in sample_docs.items():
            file_path = self.raw_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create sample sensor data
        sample_data = {
            'timestamp': pd.date_range('2024-01-01', periods=100, freq='1min'),
            'altitude': 400000 + 1000 * pd.Series(range(100)).apply(lambda x: x * 0.1),
            'battery_voltage': 28.0 - 0.01 * pd.Series(range(100)),
            'temperature': 20 + 2 * pd.Series(range(100)).apply(lambda x: (x % 10) / 10)
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(self.raw_dir / 'sample_telemetry.csv', index=False)
        
        logger.info(f"Created sample mission data in {self.raw_dir}")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of available data."""
        summary = {
            'raw_files': len(list(self.raw_dir.glob("**/*"))),
            'processed_files': len(list(self.processed_dir.glob("**/*"))),
            'synthetic_files': len(list(self.synthetic_dir.glob("**/*"))),
            'total_size': sum(f.stat().st_size for f in self.raw_dir.glob("**/*") if f.is_file())
        }
        
        return summary
