# Physics Diagnosis Module

This module contains the physics-based diagnosis functionality for the AT (Anomaly Treatment) system.

## Overview

The physics diagnosis module generates physics-based analysis of system anomalies by:
- Creating simulated telemetry data for different anomaly types
- Generating actual telemetry data with realistic noise
- Providing physics-based anomaly scoring and ranking
- Creating comprehensive diagnosis reports for the frontend

## Structure

```
physics/
├── __init__.py              # Package initialization
├── physics_diagnosis.py     # Main physics diagnosis functions
└── README.md               # This documentation
```

## Functions

### `create_physics_diagnosis_report(symptoms_list)`
Creates a complete physics diagnosis report from a list of symptoms.

**Parameters:**
- `symptoms_list`: List of symptoms from the frontend

**Returns:**
- Complete diagnosis report with physics data

### `generate_physics_diagnosis_data(symptoms_list)`
Generates physics-based diagnosis data including anomalies and telemetry.

**Parameters:**
- `symptoms_list`: List of symptoms from the frontend

**Returns:**
- Dictionary containing physics diagnosis data with anomalies, telemetry, and time labels

### `generate_actual_telemetry()`
Generates realistic actual telemetry data with noise.

**Returns:**
- List of 20 telemetry values with realistic noise

### `generate_anomaly_telemetry(anomaly_name, score)`
Generates simulated telemetry data for a specific anomaly.

**Parameters:**
- `anomaly_name`: Name of the anomaly
- `score`: Similarity score for the anomaly

**Returns:**
- List of 20 simulated telemetry values for the anomaly

## Anomaly Types

The module supports the following anomaly types with different physics effects:

- **CO₂ Scrubber Valve Leak**: Moderate effect (15 units)
- **Fan Bearing Wear**: Small effect (10 units)
- **Absorption Bed Saturated**: Large effect (20 units)
- **Heater Coil Failure**: Very large effect (25 units)
- **Pressure Sensor Drift**: Small effect (8 units)

## Usage

```python
from AT.diagnosis.physics.physics_diagnosis import create_physics_diagnosis_report

# Create a physics diagnosis report
symptoms = [{'measurement': 'ppCO2 (L1)', 'level': 'L1'}]
report = create_physics_diagnosis_report(symptoms)
```

## Integration

This module is used by the `RequestPhysicsDiagnosis` API view in `views.py` to provide physics-based diagnosis functionality to the frontend.
