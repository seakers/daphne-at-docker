import random
import math
import json
from typing import Dict, List, Any


def generate_physics_diagnosis_data(symptoms_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate physics-based diagnosis data based on symptoms.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        
    Returns:
        Dictionary containing physics diagnosis data with anomalies, telemetry, and time labels
    """
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
                'telemetry_data': generate_anomaly_telemetry('CO₂ Scrubber Valve Leak', 0.986)
            },
            {
                'name': 'Fan Bearing Wear',
                'score': '0.942',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Fan Bearing Wear', 0.942)
            },
            {
                'name': 'Absorption Bed Saturated',
                'score': '0.871',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Absorption Bed Saturated', 0.871)
            },
            {
                'name': 'Heater Coil Failure',
                'score': '0.790',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Heater Coil Failure', 0.790)
            },
            {
                'name': 'Pressure Sensor Drift',
                'score': '0.732',
                'is_highlighted': False,
                'telemetry_data': generate_anomaly_telemetry('Pressure Sensor Drift', 0.732)
            }
        ],
        'actual_telemetry': generate_actual_telemetry(),
        'time_labels': [f'T{i+1}' for i in range(20)]
    }
    
    return physics_diagnosis_data


def generate_actual_telemetry() -> List[float]:
    """
    Generate actual telemetry data with some noise.
    
    Returns:
        List of 20 telemetry values with realistic noise
    """
    actual_data = []
    for i in range(20):
        base_value = 50 + math.sin(i * 0.3) * 20
        noise = (random.random() - 0.5) * 5
        actual_data.append(base_value + noise)
    
    return actual_data


def generate_anomaly_telemetry(anomaly_name: str, score: float) -> List[float]:
    """
    Generate simulated telemetry data for a specific anomaly.
    
    Args:
        anomaly_name: Name of the anomaly
        score: Similarity score for the anomaly
        
    Returns:
        List of 20 simulated telemetry values for the anomaly
    """
    # Different anomalies have different effects
    anomaly_effects = {
        'CO₂ Scrubber Valve Leak': 15,
        'Fan Bearing Wear': 10,
        'Absorption Bed Saturated': 20,
        'Heater Coil Failure': 25,
        'Pressure Sensor Drift': 8
    }
    
    effect = anomaly_effects.get(anomaly_name, 12)
    simulated_data = []
    
    for i in range(20):
        base_value = 50 + math.sin(i * 0.3) * 20
        # Different anomalies start affecting the system at different times
        start_time = 3 + len(anomaly_name) % 5  # Vary start time based on anomaly name
        anomaly_influence = max(0, (i - start_time) / 10) * effect
        noise = (random.random() - 0.5) * 3
        simulated_data.append(base_value + anomaly_influence + noise)
    
    return simulated_data


def create_physics_diagnosis_report(symptoms_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a complete physics diagnosis report.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        
    Returns:
        Complete diagnosis report with physics data
    """
    physics_diagnosis_data = generate_physics_diagnosis_data(symptoms_list)
    
    # Build the diagnosis report and send it to the frontend
    diagnosis_report = {
        'symptoms_list': symptoms_list,
        'physics_diagnosis_data': physics_diagnosis_data,
        'diagnosis_type': 'physics'
    }
    
    return diagnosis_report
