# Container Transport Simulation

This project simulates multimodal container transport with a focus on barge transportation. It models the movement of containers between terminals using different services and transport modes.

## Features

- Container transport simulation using barges
- Terminal management with capacity constraints
- Service scheduling with pre-defined routes
- Real-time visualization of transport operations
- Performance metrics tracking
- Interactive visualization using Pygame

## Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Simulation

To run the simulation:
```bash
python main.py
```

## Project Structure

- `models.py`: Core simulation classes and logic
- `visualization.py`: Visualization components using Pygame
- `main.py`: Main simulation runner
- `requirements.txt`: Project dependencies

## Components

### Terminal
- Represents a container terminal with capacity constraints
- Handles container loading/unloading operations

### Service
- Represents a transport service between terminals
- Has defined schedule and capacity

### Barge
- Represents a transport vessel
- Has capacity and current status tracking

### Container
- Represents a shipping container (standardized to TEU)
- Tracks origin, destination, and timing requirements

## Future Extensions

1. Integration of additional transport modes (trains, trucks)
2. Advanced scheduling algorithms
3. Real-time weather and traffic conditions
4. Detailed container tracking
5. Advanced performance analytics
