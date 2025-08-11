import random
import math
import json
from typing import Dict, List, Any
from .telemetry_storage import telemetry_storage
try:
    from AT.neo4j_queries import query_functions as neo4j_q
except Exception:  # neo4j optional
    neo4j_q = None
from .cdra_sim_adapter import run_cdra_simulation, resample_series, anomaly_to_failure_config


def get_cdra_component_anomalies_from_neo4j(max_items: int = 5) -> List[str]:
    """Return a curated CDRA anomaly list.

    Note: Neo4j is intentionally disabled for now. When ready,
    uncomment the pseudo-code below to enable live queries.
    """
    fallback = [
        'CO₂ Scrubber Valve Leak',
        'Fan Bearing Wear',
        'Absorption Bed Saturated',
        'Heater Coil Failure'
        # ,
        # 'Pressure Sensor Drift'
    ]

    # Pseudo-code for future Neo4j integration (disabled):
    # if neo4j_q is not None:
    #     try:
    #         all_anoms = neo4j_q.retrieve_all_anomalies()
    #         keywords = ['co2', 'valve', 'fan', 'sorbent', 'bed', 'heater', 'pressure', 'scrubber']
    #         filtered = [a for a in all_anoms if any(k in a.lower() for k in keywords)]
    #         return (filtered or fallback)[:max_items]
    #     except Exception:
    #         pass

    return fallback[:max_items]


def _resample_labels(labels: List[str], target_len: int) -> List[str]:
    if not labels or target_len <= 0:
        return []
    if len(labels) == target_len:
        return list(labels)
    result: List[str] = []
    for i in range(target_len):
        pos = i * (len(labels) - 1) / (target_len - 1)
        idx = int(round(pos))
        result.append(labels[idx])
    return result


def _normalize_series(values: List[float]) -> List[float]:
    try:
        nums = [float(v) for v in values]
    except Exception:
        nums = [0.0 for _ in values]
    if not nums:
        return nums
    vmin = min(nums)
    vmax = max(nums)
    if vmax - vmin == 0:
        return [0.0 for _ in nums]
    return [(v - vmin) / (vmax - vmin) for v in nums]


def generate_physics_diagnosis_data(
    symptoms_list: List[Dict[str, Any]],
    target_telemetry_sensor: str = 'ppCO2 (L1)',
    sim_duration_seconds: int = 1000,
    sampling_rate_seconds: int = 10,
) -> Dict[str, Any]:
    """
    Generate physics-based diagnosis data based on symptoms.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        target_telemetry_sensor: Target telemetry sensor to analyze (default: 'ppCO2 (L1)')
        
    Returns:
        Dictionary containing physics diagnosis data with anomalies, telemetry, and time labels
    """
    # Get real telemetry data from storage for the target sensor
    telemetry_data = get_actual_telemetry_from_storage(target_telemetry_sensor, sim_duration_seconds)
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

    # Determine target points from duration and sampling rate
    target_points = max(1, int(sim_duration_seconds // max(1, int(sampling_rate_seconds))))
    # Resample actual series and labels to target_points
    effective_len = target_points
    print(f"[PHYS_DIAG] Sampling plan: duration={sim_duration_seconds}s, sample_every={sampling_rate_seconds}s -> target_points={target_points}")
    actual_telemetry = resample_series(actual_telemetry, target_points)
    time_labels = _resample_labels(time_labels, target_points)
    
    # Generate physics-based diagnosis data
    # This simulates the physics-based analysis that would be done by the backend
    # Choose anomalies (from Neo4j if available)
    cdra_anoms = get_cdra_component_anomalies_from_neo4j(max_items=5)
    # Provide synthetic descending scores for now
    comp_list = []
    actual_norm = _normalize_series(actual_telemetry)
    print(f"[PHYS_DIAG] Using {len(cdra_anoms)} anomalies; effective_len={effective_len}")
    print(f"[PHYS_DIAG] Anomaly names: {cdra_anoms}")
    
    for i, name in enumerate(cdra_anoms):
        print(f"\n[PHYS_DIAG] === Processing anomaly {i+1}/{len(cdra_anoms)}: '{name}' ===")
        sim_vals = generate_anomaly_telemetry(
            name,
            score=0.9,  # severity seed; real severity is captured by similarity metric below
            target_sensor=target_telemetry_sensor,
            duration_seconds=sim_duration_seconds,
            target_len_override=effective_len,
        )['values']
        print(f"[PHYS_DIAG] Generated {len(sim_vals)} simulation values for '{name}'")
        print(f"[PHYS_DIAG] First 10 values: {sim_vals[:10]}")
        print(f"[PHYS_DIAG] Last 10 values: {sim_vals[-10:] if len(sim_vals) >= 10 else sim_vals}")
        
        sim_norm = _normalize_series(sim_vals)
        # Mean Squared Error on normalized series
        if actual_norm and sim_norm and len(actual_norm) == len(sim_norm):
            mse = sum((a - b) ** 2 for a, b in zip(actual_norm, sim_norm)) / len(actual_norm)
        else:
            mse = 1.0
        similarity = max(0.0, min(1.0, 1.0 - mse))
        print(f"[PHYS_DIAG] anomaly='{name}', mse={mse:.4f}, similarity={similarity:.3f}")
        comp_list.append({
            'name': name,
            'score': f"{similarity:.3f}",
            'is_highlighted': False,  # set after sorting
            'telemetry_data': sim_vals,
        })
        print(f"[PHYS_DIAG] === Completed anomaly {i+1}: '{name}' ===\n")

    # Sort by similarity descending and highlight top
    comp_list.sort(key=lambda x: float(x['score']), reverse=True)
    if comp_list:
        comp_list[0]['is_highlighted'] = True

    top_prob = f"{(float(comp_list[0]['score']) * 100):.2f}%" if comp_list else '0.00%'
    print(f"[PHYS_DIAG] top_anomaly={comp_list[0]['name'] if comp_list else 'N/A'}, prob={top_prob}")
    physics_diagnosis_data = {
        'most_probable_anomaly': comp_list[0]['name'] if comp_list else 'Unknown',
        'probability': top_prob,
        'component_anomalies': comp_list,
        'actual_telemetry': actual_telemetry,
        'time_labels': time_labels,
        'telemetry_metadata': {
            'unit': unit,
            'sensor_info': sensor_info,
            'target_sensor': target_telemetry_sensor
        }
    }
    
    return physics_diagnosis_data


def get_actual_telemetry_from_storage(target_sensor: str = 'ppCO2 (L1)', sim_duration_seconds: int = 1000) -> Dict[str, Any]:
    """
    Get actual telemetry data from the storage system for a specific sensor.
    
    Args:
        target_sensor: Target sensor to extract telemetry data for (default: 'ppCO2 (L1)')
        sim_duration_seconds: Duration in seconds to fetch telemetry data for (default: 1000)
        
    Returns:
        Dictionary containing:
        - values: List of telemetry values (chronologically ordered from oldest to newest)
        - timestamps: List of timestamps (chronologically ordered from oldest to newest)
        - unit: Unit of measurement
        - sensor_info: Additional sensor information
        
    Note:
        This function collects all available telemetry data within the specified time duration.
        Since telemetry data comes almost every second, it aims to provide sim_duration_seconds
        data points. If insufficient historical data is available, it fills the beginning
        of the series with the oldest available value to reach the required length.
        This maintains chronological order: [oldest_filled_data] + [actual_historical_data]
        Data resampling is handled later in the process, not in this function.
    """
    print(f"🔍 Physics Diagnosis: Starting telemetry retrieval for sensor '{target_sensor}' for {sim_duration_seconds} seconds")
    
    try:
        # Convert duration from seconds to minutes for the telemetry storage query
        time_window_minutes = max(1, sim_duration_seconds // 60)  # Ensure at least 1 minute
        
        # Get telemetry data within the specified time window
        print(f"📊 Physics Diagnosis: Querying telemetry storage for Hera source, time window: {time_window_minutes} minutes (target: {sim_duration_seconds} data points)")
        recent_telemetry = telemetry_storage.get_telemetry_for_physics_diagnosis(source='Hera', time_window_minutes=time_window_minutes)
        # print(f"📈 Physics Diagnosis: Retrieved {len(recent_telemetry)} telemetry records from storage")
        
        if recent_telemetry:
            telemetry_values = []
            
            for i, record in enumerate(recent_telemetry):
                telemetry_data = record['data']
                #print(f"📋 Physics Diagnosis: Record {i+1} timestamp: {record['timestamp']}")
                #print(f"🔑 Physics Diagnosis: Record {i+1} keys: {list(telemetry_data.keys()) if isinstance(telemetry_data, dict) else 'Not a dict'}")
                
                if isinstance(telemetry_data, dict):
                    # Look for the target sensor specifically
                    if target_sensor in telemetry_data:
                        try:
                            value = float(telemetry_data[target_sensor])
                            telemetry_values.append(value)
                            #print(f"✅ Physics Diagnosis: Found {target_sensor} = {value} in record {i+1}")
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
            
            # If we have telemetry data, process it and handle insufficient data
            if telemetry_values:
                print(f"✅ Physics Diagnosis: Successfully retrieved {len(telemetry_values)} telemetry values for sensor '{target_sensor}'")
                print(f"📊 Physics Diagnosis: Telemetry values: initial={telemetry_values[0]}, final={telemetry_values[-1]}")
                
                # Calculate how many data points we need based on sim_duration_seconds
                # Since telemetry data comes almost every second, we need approximately sim_duration_seconds points
                target_data_points = sim_duration_seconds
                
                # If we don't have enough data, fill with the oldest available value
                if len(telemetry_values) < target_data_points:
                    print(f"⚠️ Physics Diagnosis: Insufficient data ({len(telemetry_values)} points), need {target_data_points} points")
                    print(f"🔄 Physics Diagnosis: Filling remaining data with oldest available value to the beginning of series")
                    
                    # Get the oldest value (first in the list since data is ordered by timestamp)
                    oldest_value = telemetry_values[0] if telemetry_values else 0
                    
                    # Calculate how many points we need to add
                    points_to_add = target_data_points - len(telemetry_values)
                    
                    # Add the oldest value to the beginning of the series (head)
                    # This maintains chronological order: [oldest_filled_data] + [actual_historical_data]
                    telemetry_values = [oldest_value] * points_to_add + telemetry_values
                    
                    print(f"✅ Physics Diagnosis: Extended data to {len(telemetry_values)} points by adding {points_to_add} oldest values ({oldest_value}) to the beginning")
                
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
                                #print(f"📊 Physics Diagnosis: Original Parameters: {json.dumps(original_params, indent=2)}")
                                
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
                
                # If we extended the data, also extend timestamps to match
                if len(timestamps) < len(telemetry_values):
                    print(f"🔄 Physics Diagnosis: Extending timestamps to match data length")
                    points_to_add = len(telemetry_values) - len(timestamps)
                    
                    if timestamps:
                        # Generate timestamps for the filled data at the beginning
                        # Since telemetry data comes almost every second, calculate backward from the first timestamp
                        from datetime import datetime, timedelta
                        try:
                            first_timestamp = timestamps[0]
                            if isinstance(first_timestamp, str) and 'T' in first_timestamp:
                                # Parse the first timestamp and generate earlier ones
                                base_dt = datetime.fromisoformat(first_timestamp.replace('Z', '+00:00'))
                                filled_timestamps = []
                                for i in range(points_to_add, 0, -1):  # Count backwards
                                    # Each point is 1 second apart (since telemetry comes almost every second)
                                    earlier_time = base_dt - timedelta(seconds=i)
                                    filled_timestamps.append(earlier_time.isoformat())
                                
                                # Combine: [filled_timestamps] + [original_timestamps]
                                timestamps = filled_timestamps + timestamps
                                # print(f"✅ Physics Diagnosis: Generated {len(filled_timestamps)} timestamps for filled data")
                            else:
                                # Fallback: use generic labels
                                filled_timestamps = [f"T{i+1}" for i in range(points_to_add)]
                                timestamps = filled_timestamps + timestamps
                                print(f"✅ Physics Diagnosis: Generated {len(filled_timestamps)} generic timestamps for filled data")
                        except Exception as e:
                            print(f"⚠️ Physics Diagnosis: Error generating timestamps, using fallback: {e}")
                            # Fallback: use generic labels
                            filled_timestamps = [f"T{i+1}" for i in range(points_to_add)]
                            timestamps = filled_timestamps + timestamps
                    else:
                        # No timestamps available, generate generic ones
                        filled_timestamps = [f"T{i+1}" for i in range(points_to_add)]
                        timestamps = filled_timestamps + [f"T{i+1}" for i in range(points_to_add, len(telemetry_values))]
                    
                    print(f"✅ Physics Diagnosis: Extended timestamps to {len(timestamps)} to match data length")
                
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


def generate_anomaly_telemetry(anomaly_name: str, score: float, target_sensor: str = 'ppCO2 (L1)',
                               duration_seconds: int = 60, target_len_override: int = None) -> Dict[str, Any]:
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
    print(f"[ANOMALY_TELEMETRY] Generating telemetry for anomaly: '{anomaly_name}'")
    # print(f"[ANOMALY_TELEMETRY] Parameters: score={score}, duration={duration_seconds}s, target_len={target_len_override}")

    # Build failure config from anomaly name and score
    failure_cfg = anomaly_to_failure_config(anomaly_name, severity=float(score))
    # print(f"[ANOMALY_TELEMETRY] Failure config generated: {failure_cfg}")

    baseline = 3.0 #[mmHg] reasonable ppCO2 partial pressure baseline placeholder
    print(f"[ANOMALY_TELEMETRY] Using baseline CO2: {baseline} mmHg")

    # Run simulator (dt fixed at 1s as requested)
    print(f"[ANOMALY_TELEMETRY] Starting CDRA simulation...")
    raw_series = run_cdra_simulation(
        failure_config=failure_cfg,
        duration_seconds= duration_seconds,
        baseline_co2_mmHg=baseline,
        onset_time_sec=3,
    )
    print(f"[ANOMALY_TELEMETRY] CDRA simulation completed, generated {len(raw_series)} points")
    # print(f"[ANOMALY_TELEMETRY] Raw series range: {min(raw_series):.4f} to {max(raw_series):.4f} mmHg")

    # Resample to the same number of points as actual data 
    if target_len_override:
        # print(f"[ANOMALY_TELEMETRY] Resampling from {len(raw_series)} to {target_len_override} points")
        resampled = resample_series(raw_series, target_len_override)
        print(f"[ANOMALY_TELEMETRY] Resampled series range: {min(resampled):.4f} to {max(resampled):.4f} mmHg")
    else:
        resampled = raw_series
        print(f"[ANOMALY_TELEMETRY] No resampling needed")

    return {
        'values': resampled,
        # 'timestamps': telemetry_data.get('timestamps', []),
        # 'unit': telemetry_data.get('unit', '')
    }


def create_physics_diagnosis_report(
    symptoms_list: List[Dict[str, Any]],
    target_telemetry_sensor: str = 'ppCO2 (L1)',
    sim_duration_seconds: int = 1000,
    sampling_rate_seconds: int = 10,
) -> Dict[str, Any]:
    """
    Create a complete physics diagnosis report.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        target_telemetry_sensor: Target telemetry sensor to analyze (default: 'ppCO2 (L1)')
        
    Returns:
        Complete diagnosis report with physics data
    """
    physics_diagnosis_data = generate_physics_diagnosis_data(symptoms_list, target_telemetry_sensor, sim_duration_seconds, sampling_rate_seconds)
    
    # Build the diagnosis report and send it to the frontend
    diagnosis_report = {
        'symptoms_list': symptoms_list,
        'physics_diagnosis_data': physics_diagnosis_data,
        'diagnosis_type': 'physics',
        'target_telemetry_sensor': target_telemetry_sensor,
        'simulation': {
            'duration_seconds': sim_duration_seconds,
            'dt_seconds': 1,
            'sampling_rate_seconds': sampling_rate_seconds,
            'points': len(physics_diagnosis_data['actual_telemetry'])
        }
    }
    
    return diagnosis_report
