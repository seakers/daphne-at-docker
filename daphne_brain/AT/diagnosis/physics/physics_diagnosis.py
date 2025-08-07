import random
import math
import json
from typing import Dict, List, Any
from .telemetry_storage import telemetry_storage


def generate_physics_diagnosis_data(symptoms_list: List[Dict[str, Any]], target_telemetry_sensor: str = 'ppCO2 (L1)') -> Dict[str, Any]:
    """
    Generate physics-based diagnosis data based on symptoms.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        target_telemetry_sensor: Target telemetry sensor to analyze (default: 'ppCO2 (L1)')
        
    Returns:
        Dictionary containing physics diagnosis data with anomalies, telemetry, and time labels
    """
    # Get real telemetry data from storage for the target sensor
    telemetry_data = get_actual_telemetry_from_storage(target_telemetry_sensor)
    actual_telemetry = telemetry_data['values']
    timestamps = telemetry_data['timestamps']
    unit = telemetry_data['unit']
    sensor_info = telemetry_data['sensor_info']
    
    # Generate time labels based on timestamps or fallback to T1, T2, etc.
    if timestamps:
        # Convert timestamps to readable format (e.g., "14:30:45")
        from datetime import datetime
        time_labels = []
        for ts in timestamps:
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                time_labels.append(dt.strftime('%H:%M:%S'))
            except (ValueError, AttributeError):
                time_labels.append(ts)  # Use raw timestamp if parsing fails
    else:
        time_labels = generate_time_labels(len(actual_telemetry))
    
    # Generate physics-based diagnosis data
    # This simulates the physics-based analysis that would be done by the backend
    physics_diagnosis_data = {
        'most_probable_anomaly': 'CDRA Failure',
        'probability': '88.73%',
        'component_anomalies': [
            {
                'name': 'CO₂ Scrubber Valve Leak',
                'score': '0.986',
                'is_highlighted': True,
                'telemetry_data': generate_anomaly_telemetry('CO₂ Scrubber Valve Leak', 0.986, target_telemetry_sensor)['values']
            },
            {
                'name': 'Fan Bearing Wear',
                'score': '0.942',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Fan Bearing Wear', 0.942, target_telemetry_sensor)['values']
            },
            {
                'name': 'Absorption Bed Saturated',
                'score': '0.871',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Absorption Bed Saturated', 0.871, target_telemetry_sensor)['values']
            },
            {
                'name': 'Heater Coil Failure',
                'score': '0.790',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Heater Coil Failure', 0.790, target_telemetry_sensor)['values']
            },
            {
                'name': 'Pressure Sensor Drift',
                'score': '0.732',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Pressure Sensor Drift', 0.732, target_telemetry_sensor)['values']
            }
        ],
        'actual_telemetry': actual_telemetry,
        'time_labels': time_labels,
        'telemetry_metadata': {
            'unit': unit,
            'sensor_info': sensor_info,
            'target_sensor': target_telemetry_sensor
        }
    }
    
    return physics_diagnosis_data


def get_actual_telemetry_from_storage(target_sensor: str = 'ppCO2 (L1)') -> Dict[str, Any]:
    """
    Get actual telemetry data from the storage system for a specific sensor.
    
    Args:
        target_sensor: Target sensor to extract telemetry data for (default: 'ppCO2 (L1)')
        
    Returns:
        Dictionary containing:
        - values: List of telemetry values
        - timestamps: List of timestamps
        - unit: Unit of measurement
        - sensor_info: Additional sensor information
    """
    print(f"🔍 Physics Diagnosis: Starting telemetry retrieval for sensor '{target_sensor}'")
    
    try:
        # Get recent telemetry data (last 20 readings)
        print(f"📊 Physics Diagnosis: Querying telemetry storage for Hera source, limit 20")
        recent_telemetry = telemetry_storage.get_recent_telemetry(source='Hera', limit=20)
        print(f"📈 Physics Diagnosis: Retrieved {len(recent_telemetry)} telemetry records from storage")
        
        if recent_telemetry:
            telemetry_values = []
            
            for i, record in enumerate(recent_telemetry):
                telemetry_data = record['data']
                print(f"📋 Physics Diagnosis: Record {i+1} timestamp: {record['timestamp']}")
                print(f"🔑 Physics Diagnosis: Record {i+1} keys: {list(telemetry_data.keys()) if isinstance(telemetry_data, dict) else 'Not a dict'}")
                
                if isinstance(telemetry_data, dict):
                    # Look for the target sensor specifically
                    if target_sensor in telemetry_data:
                        try:
                            value = float(telemetry_data[target_sensor])
                            telemetry_values.append(value)
                            print(f"✅ Physics Diagnosis: Found {target_sensor} = {value} in record {i+1}")
                        except (ValueError, TypeError) as e:
                            print(f"❌ Physics Diagnosis: Could not convert {target_sensor} value to float: {telemetry_data[target_sensor]} (Error: {e})")
                            continue
                    else:
                        print(f"❌ Physics Diagnosis: Target sensor '{target_sensor}' not found in record {i+1}")
                        # If target sensor not found, try alternative names
                        alternative_sensors = get_alternative_sensor_names(target_sensor)
                        print(f"🔍 Physics Diagnosis: Trying alternative sensors: {alternative_sensors}")
                        for alt_sensor in alternative_sensors:
                            if alt_sensor in telemetry_data:
                                try:
                                    value = float(telemetry_data[alt_sensor])
                                    telemetry_values.append(value)
                                    print(f"✅ Physics Diagnosis: Using alternative sensor '{alt_sensor}' = {value} for '{target_sensor}' in record {i+1}")
                                    break
                                except (ValueError, TypeError) as e:
                                    print(f"❌ Physics Diagnosis: Could not convert alternative sensor '{alt_sensor}' value: {telemetry_data[alt_sensor]} (Error: {e})")
                                    continue
                        else:
                            print(f"❌ Physics Diagnosis: No alternative sensors found in record {i+1}")
                else:
                    print(f"❌ Physics Diagnosis: Record {i+1} data is not a dictionary: {type(telemetry_data)}")
            
            # If we have telemetry data, return it with metadata
            if telemetry_values:
                print(f"✅ Physics Diagnosis: Successfully retrieved {len(telemetry_values)} telemetry values for sensor '{target_sensor}'")
                print(f"📊 Physics Diagnosis: Telemetry values: {telemetry_values}")
                
                # Extract timestamps and sensor info from the first record that had valid data
                timestamps = []
                unit = None
                sensor_info = None
                
                for record in recent_telemetry:
                    telemetry_data = record['data']
                    if isinstance(telemetry_data, dict):
                        # Look for the target sensor or its alternatives
                        found_sensor = None
                        if target_sensor in telemetry_data:
                            found_sensor = target_sensor
                        else:
                            for alt_sensor in get_alternative_sensor_names(target_sensor):
                                if alt_sensor in telemetry_data:
                                    found_sensor = alt_sensor
                                    break
                        
                        if found_sensor:
                            timestamps.append(record['timestamp'])
                            # If we haven't found unit/info yet, look for it in the original Parameters list
                            if unit is None and 'metadata' in record and 'original_data' in record['metadata'] and 'Parameters' in record['metadata']['original_data']:
                                print(f"🔍 Physics Diagnosis: Looking for sensor info in original data")
                                original_params = record['metadata']['original_data']['Parameters']
                                print(f"📊 Physics Diagnosis: Original Parameters: {json.dumps(original_params, indent=2)}")
                                
                                target_name = found_sensor.split(' (')[0]
                                target_group = found_sensor.split('(')[1].strip(')')
                                print(f"🎯 Physics Diagnosis: Looking for Name={target_name}, ParameterGroup={target_group}")
                                
                                for param in original_params:
                                    if isinstance(param, dict) and param.get('Name') == target_name and param.get('ParameterGroup') == target_group:
                                        unit = param.get('Unit', '')
                                        sensor_info = {
                                            'nominal_value': param.get('NominalValue'),
                                            'upper_caution': param.get('UpperCautionLimit'),
                                            'upper_warning': param.get('UpperWarningLimit'),
                                            'lower_caution': param.get('LowerCautionLimit'),
                                            'lower_warning': param.get('LowerWarningLimit')
                                        }
                                        print(f"✅ Physics Diagnosis: Found sensor info - Unit: {unit}, Info: {sensor_info}")
                                        break
                                else:
                                    print(f"❌ Physics Diagnosis: No matching sensor found in original data")
                
                return {
                    'values': telemetry_values,
                    'timestamps': timestamps,
                    'unit': unit or 'unknown',
                    'sensor_info': sensor_info or {}
                }
            else:
                print(f"❌ Physics Diagnosis: No valid telemetry values found for sensor '{target_sensor}'")
        else:
            print(f"❌ Physics Diagnosis: No telemetry records found in storage")
        
        # Fallback to generated data if no real telemetry available
        print(f"⚠️ Physics Diagnosis: No real telemetry data available for '{target_sensor}', using generated data")
        generated_data = generate_actual_telemetry()
        print(f"🔄 Physics Diagnosis: Generated {len(generated_data)} fallback values")
        return {
            'values': generated_data,
            'timestamps': [f"T{i+1}" for i in range(len(generated_data))],
            'unit': 'unknown',
            'sensor_info': {}
        }
        
    except Exception as e:
        print(f"❌ Physics Diagnosis: Error retrieving telemetry data for '{target_sensor}': {e}")
        import traceback
        traceback.print_exc()
        # Fallback to generated data
        generated_data = generate_actual_telemetry()
        print(f"🔄 Physics Diagnosis: Using generated data due to error")
        return {
            'values': generated_data,
            'timestamps': [f"T{i+1}" for i in range(len(generated_data))],
            'unit': 'unknown',
            'sensor_info': {}
        }


def get_alternative_sensor_names(target_sensor: str) -> List[str]:
    """
    Get alternative sensor names for a target sensor.
    
    Args:
        target_sensor: The target sensor name
        
    Returns:
        List of alternative sensor names to try
    """
    # Define alternative sensor names for common sensors
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
    
    return sensor_alternatives.get(target_sensor, [])


def generate_actual_telemetry() -> List[float]:
    """
    Generate actual telemetry data with some noise.
    This is used as a fallback when no real telemetry data is available.
    
    Returns:
        List of 20 telemetry values with realistic noise
    """
    actual_data = []
    for i in range(20):
        base_value = 50 + math.sin(i * 0.3) * 20
        noise = (random.random() - 0.5) * 5
        actual_data.append(base_value + noise)
    
    return actual_data


def generate_time_labels(data_length: int) -> List[str]:
    """
    Generate time labels for the telemetry data.
    
    Args:
        data_length: Number of data points
        
    Returns:
        List of time labels
    """
    return [f'T{i+1}' for i in range(data_length)]


def generate_anomaly_telemetry(anomaly_name: str, score: float, target_sensor: str = 'ppCO2 (L1)') -> Dict[str, Any]:
    """
    Generate simulated telemetry data for a specific anomaly.
    
    Args:
        anomaly_name: Name of the anomaly
        score: Similarity score for the anomaly
        target_sensor: Target sensor to simulate (default: 'ppCO2 (L1)')
        
    Returns:
        Dictionary containing:
        - values: List of simulated telemetry values
        - timestamps: List of timestamps (copied from actual data)
        - unit: Unit of measurement
    """
    # Get actual telemetry data to base simulation on
    telemetry_data = get_actual_telemetry_from_storage(target_sensor)
    actual_values = telemetry_data['values']
    data_length = len(actual_values)
    
    # Calculate the scale factor based on the real telemetry values
    if actual_values:
        # Convert all values to float to ensure numeric operations work
        numeric_values = [float(v) for v in actual_values]
        avg_value = sum(numeric_values) / len(numeric_values)
        # Scale the anomaly effects to be proportional to the real telemetry values
        # Use 10-20% of the average value as the maximum effect
        max_effect_percentage = 0.15  # 15% of average value
        scale_factor = avg_value * max_effect_percentage
    else:
        scale_factor = 1.0
    
    # Define anomaly effects as percentages of the scale factor
    anomaly_effects = {
        'CO₂ Scrubber Valve Leak': 0.8,    # 80% of scale factor
        'Fan Bearing Wear': 0.5,            # 50% of scale factor
        'Absorption Bed Saturated': 1.0,    # 100% of scale factor
        'Heater Coil Failure': 1.2,         # 120% of scale factor
        'Pressure Sensor Drift': 0.4        # 40% of scale factor
    }
    
    effect_percentage = anomaly_effects.get(anomaly_name, 0.5)
    effect = scale_factor * effect_percentage
    
    simulated_values = []
    
    for i in range(data_length):
        if i < len(actual_values):
            try:
                base_value = float(actual_values[i])
            except (ValueError, TypeError):
                # Fallback if value can't be converted to float
                base_value = 50 + math.sin(i * 0.3) * 20
        else:
            # Fallback if actual data is shorter than expected
            base_value = 50 + math.sin(i * 0.3) * 20
        
        # Different anomalies start affecting the system at different times
        start_time = 3 + len(anomaly_name) % 5  # Vary start time based on anomaly name
        anomaly_influence = max(0, (i - start_time) / 10) * effect * score
        noise = (random.random() - 0.5) * effect * 0.1  # Reduced noise
        simulated_values.append(base_value + anomaly_influence + noise)
    
    return {
        'values': simulated_values,
        'timestamps': telemetry_data.get('timestamps', []),
        'unit': telemetry_data.get('unit', '')
    }


def create_physics_diagnosis_report(symptoms_list: List[Dict[str, Any]], target_telemetry_sensor: str = 'ppCO2 (L1)') -> Dict[str, Any]:
    """
    Create a complete physics diagnosis report.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        target_telemetry_sensor: Target telemetry sensor to analyze (default: 'ppCO2 (L1)')
        
    Returns:
        Complete diagnosis report with physics data
    """
    physics_diagnosis_data = generate_physics_diagnosis_data(symptoms_list, target_telemetry_sensor)
    
    # Build the diagnosis report and send it to the frontend
    diagnosis_report = {
        'symptoms_list': symptoms_list,
        'physics_diagnosis_data': physics_diagnosis_data,
        'diagnosis_type': 'physics',
        'target_telemetry_sensor': target_telemetry_sensor
    }
    
    return diagnosis_report
