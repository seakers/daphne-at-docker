# Physics Diagnosis Module

This module contains the physics-based diagnosis functionality for the AT (Anomaly Treatment) system.

## Overview

The physics diagnosis module generates physics-based analysis of system anomalies by:
- Creating simulated telemetry data for different anomaly types
- **Using real historical telemetry data from the Hera simulator**
- Generating actual telemetry data with realistic noise (fallback)
- Providing physics-based anomaly scoring and ranking
- Creating comprehensive diagnosis reports for the frontend

## Structure

```
physics/
├── __init__.py              # Package initialization
├── physics_diagnosis.py     # Main physics diagnosis functions
├── telemetry_storage.py     # Telemetry storage and retrieval service
└── README.md               # This documentation
```

## Telemetry Storage System

### **Historical Telemetry Storage**
The system now stores real telemetry data from the Hera simulator for use in physics diagnosis:

- **Automatic Storage**: Every telemetry reading from `HeraFeed` API is automatically stored
- **Database Model**: `TelemetryHistory` model stores telemetry data with timestamps
- **Efficient Retrieval**: Indexed queries for fast access to recent telemetry data
- **Data Cleanup**: Automatic cleanup of old telemetry data to prevent database bloat

### **Storage Features**
- **Real-time Storage**: Telemetry data is stored immediately when received
- **Time-series Data**: Historical telemetry data for trend analysis
- **Multi-source Support**: Can store telemetry from different sources (Hera, sEclss, etc.)
- **Session Tracking**: Groups telemetry data by session for multi-user scenarios
- **Metadata Support**: Additional context information for each telemetry reading

## Functions

### **Physics Diagnosis Functions**

#### `create_physics_diagnosis_report(symptoms_list, target_telemetry_sensor)`
Creates a complete physics diagnosis report from a list of symptoms.

**Parameters:**
- `symptoms_list`: List of symptoms from the frontend
- `target_telemetry_sensor`: Target telemetry sensor to analyze (default: 'ppCO2 (L1)')

**Returns:**
- Complete diagnosis report with physics data

#### `generate_physics_diagnosis_data(symptoms_list, target_telemetry_sensor)`
Generates physics-based diagnosis data including anomalies and telemetry.

**Parameters:**
- `symptoms_list`: List of symptoms from the frontend
- `target_telemetry_sensor`: Target telemetry sensor to analyze (default: 'ppCO2 (L1)')

**Returns:**
- Dictionary containing physics diagnosis data with anomalies, telemetry, and time labels

#### `get_actual_telemetry_from_storage(target_sensor)`
Retrieves real telemetry data from the storage system for physics diagnosis.

**Parameters:**
- `target_sensor`: Target sensor to extract telemetry data for (default: 'ppCO2 (L1)')

**Returns:**
- List of telemetry values from the last 20 readings for the target sensor
- Falls back to generated data if no real telemetry is available

#### `generate_actual_telemetry()`
Generates realistic actual telemetry data with noise (fallback method).

**Returns:**
- List of 20 telemetry values with realistic noise

#### `generate_anomaly_telemetry(anomaly_name, score, target_sensor)`
Generates simulated telemetry data for a specific anomaly based on real telemetry.

**Parameters:**
- `anomaly_name`: Name of the anomaly
- `score`: Similarity score for the anomaly
- `target_sensor`: Target sensor to simulate (default: 'ppCO2 (L1)')

**Returns:**
- List of simulated telemetry values for the anomaly

### **Telemetry Storage Functions**

#### `TelemetryStorageService.store_telemetry(telemetry_data, source, user_information, metadata)`
Stores telemetry data in the database.

**Parameters:**
- `telemetry_data`: Dictionary containing telemetry readings
- `source`: Source of the telemetry data (default: 'Hera')
- `user_information`: Optional user information object
- `metadata`: Optional metadata dictionary

**Returns:**
- TelemetryHistory object that was created

#### `TelemetryStorageService.get_recent_telemetry(source, limit)`
Gets recent telemetry data for physics diagnosis.

**Parameters:**
- `source`: Source of telemetry data (default: 'Hera')
- `limit`: Number of recent readings to retrieve (default: 100)

**Returns:**
- List of telemetry data dictionaries

#### `TelemetryStorageService.get_telemetry_for_physics_diagnosis(source, time_window_minutes)`
Gets telemetry data within a time window for physics diagnosis.

**Parameters:**
- `source`: Source of telemetry data (default: 'Hera')
- `time_window_minutes`: Time window in minutes (default: 60)

**Returns:**
- List of telemetry data dictionaries within the time window

#### `TelemetryStorageService.get_telemetry_timeseries(source, time_window_minutes, sensor_keys)`
Gets telemetry data as a time series for physics diagnosis.

**Parameters:**
- `source`: Source of telemetry data (default: 'Hera')
- `time_window_minutes`: Time window in minutes (default: 60)
- `sensor_keys`: Optional list of sensor keys to extract

**Returns:**
- Dictionary with sensor names as keys and lists of values as values

#### `TelemetryStorageService.cleanup_old_telemetry(days_to_keep)`
Cleans up old telemetry data to prevent database bloat.

**Parameters:**
- `days_to_keep`: Number of days of data to keep (default: 7)

**Returns:**
- Number of records deleted

## Anomaly Types

The module supports the following anomaly types with different physics effects:

- **CO₂ Scrubber Valve Leak**: Moderate effect (15 units)
- **Fan Bearing Wear**: Small effect (10 units)
- **Absorption Bed Saturated**: Large effect (20 units)
- **Heater Coil Failure**: Very large effect (25 units)
- **Pressure Sensor Drift**: Small effect (8 units)

## Target Telemetry Configuration

### **Configurable Target Sensor**
The physics diagnosis system now supports configurable target telemetry sensors:

- **Default Target**: `'ppCO2 (L1)'` - Carbon dioxide level sensor
- **Easy Configuration**: Change target sensor in `RequestPhysicsDiagnosis` class
- **Alternative Names**: Automatic fallback to alternative sensor names
- **Flexible**: Can target any telemetry sensor available in the system

### **Alternative Sensor Names**
The system automatically tries alternative names if the exact sensor name is not found:

```python
sensor_alternatives = {
    'ppCO2 (L1)': ['ppCO2 (L1)', 'ppCO2 (L2)', 'ppCO2', 'CO2', 'Carbon Dioxide', 'CO2 Level'],
    'Cabin Temperature (L1)': ['Cabin Temperature (L1)', 'Cabin Temperature (L2)', 'Temperature', 'Temp', 'Cabin Temp'],
    'Humidity (L1)': ['Humidity (L1)', 'Humidity (L2)', 'Humidity Level', 'Relative Humidity', 'RH'],
    'Pressure (L1)': ['Pressure (L1)', 'Pressure (L2)', 'Cabin Pressure', 'Atmospheric Pressure', 'Air Pressure'],
    'ppO2 (L1)': ['ppO2 (L1)', 'ppO2 (L2)', 'Oxygen', 'O2', 'Oxygen Level'],
    'ppN2 (L1)': ['ppN2 (L1)', 'ppN2 (L2)', 'Nitrogen', 'N2', 'Nitrogen Level'],
    'ppH2 (L1)': ['ppH2 (L1)', 'ppH2 (L2)', 'Hydrogen', 'H2', 'Hydrogen Level'],
    'H2O (L1)': ['H2O (L1)', 'H2O (L2)', 'Water Vapor', 'Moisture', 'Water Level']
}
```

### **Data Structure**
The telemetry data comes from the Hera simulator in the following format:
```json
{
  "Parameters": [
    {
      "Id": 38,
      "Name": "ppCO2",
      "ParameterGroup": "L1",
      "currentValue": 2.59,
      "NominalValue": 2.59,
      "Unit": "mmHG",
      // ... other properties
    },
    // ... more sensors
  ]
}
```

The system converts this list structure to a dictionary format for easier access:
```python
{
  "ppCO2 (L1)": 2.59,
  "ppCO2 (L2)": 2.59,
  "Cabin Temperature (L1)": 72.302,
  // ... etc
}
```

### **Dynamic Scaling System**
The physics diagnosis system now includes intelligent scaling to handle different telemetry value ranges:

#### **Backend Scaling**
- **Proportional Effects**: Anomaly effects are scaled as a percentage of the actual telemetry values
- **Scale Factor**: Calculated as 15% of the average telemetry value
- **Effect Percentages**:
  - CO₂ Scrubber Valve Leak: 80% of scale factor
  - Fan Bearing Wear: 50% of scale factor
  - Absorption Bed Saturated: 100% of scale factor
  - Heater Coil Failure: 120% of scale factor
  - Pressure Sensor Drift: 40% of scale factor

#### **Frontend Scaling**
- **Dynamic Y-Axis**: Automatically calculates the range based on all data points
- **Padding**: Adds 10% padding above and below the data range
- **Real-time Adjustment**: Graph scales to accommodate both actual and simulated data
- **Fallback**: Uses fixed range (0-100) if dynamic calculation fails

#### **Example Scaling**
For telemetry values around 6 mmHg:
- **Scale Factor**: 6 × 0.15 = 0.9
- **Anomaly Effects**: 0.4 to 1.08 units (instead of fixed 8-25 units)
- **Graph Range**: Automatically adjusts to show 5-8 mmHg range

## Usage

### **Basic Physics Diagnosis**
```python
from AT.diagnosis.physics.physics_diagnosis import create_physics_diagnosis_report

# Create a physics diagnosis report with default target sensor (ppCO2 L1)
symptoms = [{'measurement': 'ppCO2 (L1)', 'level': 'L1'}]
report = create_physics_diagnosis_report(symptoms)

# Create a physics diagnosis report with custom target sensor
report = create_physics_diagnosis_report(symptoms, target_telemetry_sensor='Cabin Temperature')
```

### **Telemetry Storage**
```python
from AT.diagnosis.physics.telemetry_storage import telemetry_storage

# Store telemetry data
telemetry_data = {'Cabin Temperature': 25.5, 'ppCO2': 0.04}
telemetry_storage.store_telemetry(telemetry_data, source='Hera')

# Get recent telemetry for physics diagnosis
recent_data = telemetry_storage.get_recent_telemetry(source='Hera', limit=20)
```

### **Time Series Analysis**
```python
# Get telemetry as time series
timeseries = telemetry_storage.get_telemetry_timeseries(
    source='Hera',
    time_window_minutes=60,
    sensor_keys=['Cabin Temperature', 'ppCO2']
)
```

## Integration

### **Backend Integration**
- **HeraFeed API**: Automatically stores telemetry data when received
- **Physics Diagnosis**: Uses real telemetry data for diagnosis reports
- **Database**: Persistent storage with automatic cleanup

### **Frontend Integration**
- **Real Telemetry**: Physics diagnosis now uses actual telemetry trends
- **Historical Data**: Access to historical telemetry for trend analysis
- **Fallback Support**: Graceful fallback to generated data when needed

## Database Schema

### **TelemetryHistory Model**
```sql
CREATE TABLE AT_telemetryhistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    telemetry_data JSON NOT NULL,
    source VARCHAR(50) DEFAULT 'Hera',
    session_id VARCHAR(100) NULL,
    metadata JSON DEFAULT '{}',
    user_information_id INTEGER NULL,
    FOREIGN KEY (user_information_id) REFERENCES daphne_context_userinformation(id)
);
```

### **Indexes**
- `timestamp`: For efficient time-based queries
- `source, timestamp`: For source-specific time queries
- `session_id, timestamp`: For session-specific queries

## Performance Considerations

- **Automatic Cleanup**: Old telemetry data is automatically cleaned up
- **Indexed Queries**: Fast retrieval of recent telemetry data
- **Memory Efficient**: Only stores necessary telemetry data
- **Fallback Support**: Graceful degradation when real data is unavailable

This module is used by the `RequestPhysicsDiagnosis` API view in `views.py` to provide physics-based diagnosis functionality to the frontend with real telemetry data.
