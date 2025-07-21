# 🚀 Netra - Space Flight Simulation & RAG Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Netra** is a comprehensive space flight simulation and Retrieval Augmented Generation (RAG) platform that combines real-time orbital mechanics simulation with AI-powered mission assistance.

## ✨ Features

### 🛰️ Space Flight Simulation
- **Real-time orbital mechanics**: Physics-based simulation with gravitational forces, atmospheric drag, and fuel consumption
- **Interactive parameter control**: Adjust spacecraft mass, thrust, orbital parameters in real-time
- **Multiple mission scenarios**: Support for various orbital configurations and mission types
- **State management**: Complete tracking of spacecraft position, velocity, and system status

### 📡 Synthetic Sensor Data
- **20+ sensor types**: IMU, GPS, environmental, power, propulsion, and communication sensors
- **Realistic noise and drift**: Configurable sensor accuracy, noise levels, and failure simulation
- **Time-series data generation**: Continuous sensor readings with proper temporal relationships
- **Sensor health monitoring**: Track sensor status, failures, and repair operations

### 📊 Real-time Visualization
- **3D trajectory plotting**: Interactive 3D visualization of spacecraft orbit around Earth
- **Live telemetry dashboard**: Real-time charts for altitude, speed, power, temperature, and more
- **Mission status indicators**: Visual status displays and alert systems
- **Parameter monitoring**: Track fuel levels, battery voltage, radiation exposure

### 🤖 AI-Powered Mission Assistant (RAG)
- **Document-based knowledge**: Query mission procedures, spacecraft specifications, and orbital mechanics
- **Context-aware responses**: Incorporates current mission status into AI responses
- **Vector database storage**: ChromaDB for efficient document retrieval and semantic search
- **OpenAI integration**: GPT-4 powered natural language interface

### 🎮 Interactive Interface
- **Streamlit web app**: Modern, responsive web interface
- **Real-time controls**: Start, pause, reset, and step through simulations
- **Parameter adjustment**: Live modification of simulation parameters
- **Auto-refresh mode**: Continuous simulation updates with configurable refresh rates

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- OpenAI API key (for RAG functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd netra
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   
   This will:
   - Install all required dependencies
   - Create necessary directories
   - Initialize sample mission data
   - Set up environment configuration

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Launch the application**
   ```bash
   streamlit run app.py
   ```
   
   Or directly:
   ```bash
   python -m streamlit run src/ui/main_app.py
   ```

The application will open in your web browser at `http://localhost:8501`.

## 🎯 Usage Guide

### Starting a Simulation

1. **Configure Parameters**: Use the sidebar to adjust spacecraft and mission parameters
2. **Start Simulation**: Click the "▶️ Start Simulation" button
3. **Monitor Progress**: Watch real-time telemetry and 3D trajectory visualization
4. **Interact with AI**: Ask questions about the mission using the RAG assistant

### Key Interface Elements

- **Simulation Tab**: Main control panel with status indicators and latest sensor readings
- **Telemetry Tab**: Real-time charts and graphs of sensor data
- **Trajectory Tab**: 3D visualization of spacecraft orbit
- **Mission Assistant Tab**: AI-powered chat interface for mission support

### Example Interactions

**Physics Simulation:**
- Adjust spacecraft mass to see orbital changes
- Monitor fuel consumption during maneuvers
- Observe atmospheric drag effects at different altitudes

**Sensor Data:**
- Watch real-time sensor readings update
- Simulate sensor failures and observe system response
- Export sensor data for analysis

**AI Assistant:**
- "What is the current orbital period?"
- "How much fuel do we have remaining?"
- "What should I do if sensors start failing?"

## 🏗️ Architecture

### Project Structure
```
netra/
├── src/
│   ├── physics/          # Simulation engine and sensor data
│   │   ├── simulation.py    # Orbital mechanics simulation
│   │   └── sensors.py       # Synthetic sensor data generation
│   ├── rag/              # RAG system implementation
│   │   └── core.py          # LlamaIndex + ChromaDB integration
│   ├── ui/               # Streamlit interface
│   │   ├── main_app.py      # Main application
│   │   └── components.py    # Reusable UI components
│   └── data/             # Data management
│       ├── loader.py        # Document loading utilities
│       └── synthetic.py     # Synthetic data generation
├── data/                 # Data storage
│   ├── raw/              # Mission documents and specifications
│   ├── processed/        # Processed data files
│   ├── synthetic/        # Generated synthetic data
│   └── chroma_db/        # Vector database storage
├── requirements.txt      # Python dependencies
├── setup.py             # Setup and installation script
└── app.py               # Main entry point
```

### Technology Stack

**Core Frameworks:**
- **Streamlit**: Web interface and real-time visualization
- **LlamaIndex**: RAG implementation and document processing
- **ChromaDB**: Vector database for semantic search
- **OpenAI**: LLM integration for natural language processing

**Scientific Computing:**
- **NumPy**: Numerical computations and array operations
- **Pandas**: Data manipulation and time-series handling
- **SciPy**: Advanced mathematical functions
- **Plotly**: Interactive 3D visualization and charts

**Data Management:**
- **Python-dotenv**: Environment configuration
- **Pathlib**: Cross-platform file operations
- **JSON/CSV**: Data serialization and storage

## 📈 Simulation Details

### Physics Model
- **Gravitational Force**: Newton's law of universal gravitation
- **Atmospheric Drag**: Exponential atmosphere model with configurable density
- **Orbital Mechanics**: Keplerian orbits with perturbations
- **Fuel Consumption**: Realistic thrust-to-fuel consumption ratios

### Sensor Types
- **Navigation**: GPS, altitude, attitude determination
- **Inertial**: 3-axis accelerometer and gyroscope
- **Environmental**: Internal/external temperature, radiation, cabin pressure
- **Power**: Battery voltage, solar panel current, power consumption
- **Propulsion**: Fuel level, thrust magnitude, engine temperature
- **Communication**: Signal strength, data rate, link quality

### Default Parameters
- **Initial Orbit**: 400 km altitude circular orbit
- **Spacecraft Mass**: 1000 kg
- **Fuel Capacity**: 500 kg
- **Maximum Thrust**: 10,000 N
- **Mission Duration**: 1-24 hours (configurable)

## 🤖 RAG System

The Retrieval Augmented Generation system provides intelligent mission assistance by:

1. **Document Processing**: Ingests mission documents, procedures, and specifications
2. **Vector Storage**: Creates embeddings using OpenAI's text-embedding models
3. **Semantic Search**: ChromaDB enables fast similarity-based document retrieval
4. **Context Integration**: Combines retrieved documents with current mission status
5. **AI Response**: GPT-4 generates contextually relevant answers and recommendations

### Sample Queries
- Technical questions about orbital mechanics
- Mission procedure lookups
- Real-time status interpretations
- Troubleshooting guidance
- Parameter recommendation

## 🔧 Configuration

### Environment Variables (.env)
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Simulation Configuration
DEFAULT_MISSION_DURATION=3600
DEFAULT_TIME_STEP=1.0

# RAG Configuration
CHROMA_DB_PATH=./data/chroma_db
RAG_COLLECTION_NAME=space_missions
```

### Streamlit Configuration (.streamlit/config.toml)
- Custom theme colors
- Server settings
- Development mode options

## 📊 Data Export

The platform supports exporting:
- **Simulation trajectories**: CSV/JSON format with position, velocity, and time data
- **Sensor readings**: Time-series data with all sensor measurements
- **Mission reports**: Automated report generation with statistics and analysis
- **Anomaly logs**: Sensor failures and system events

## 🛠️ Development

### Adding New Sensors
1. Define sensor configuration in `SensorConfig`
2. Implement true value calculation in `_calculate_true_value()`
3. Configure noise and failure parameters
4. Update UI components for display

### Extending Physics Model
- Add new force calculations to `SpaceFlightSimulation`
- Implement additional orbital perturbations
- Include more sophisticated atmosphere models
- Add spacecraft component modeling

### Customizing RAG System
- Add new document types to `DataLoader`
- Implement custom embedding strategies
- Extend query processing pipeline
- Add specialized knowledge domains

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you have questions or need help:
1. Check the documentation in the `/notes` directory
2. Review the sample data and configurations
3. Open an issue for bug reports or feature requests

---

**Built with ❤️ for space exploration and simulation**