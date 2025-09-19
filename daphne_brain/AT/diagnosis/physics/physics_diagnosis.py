import random
import math
import numpy as np
import json
import os
from typing import Dict, List, Any
from sklearn.metrics import mean_squared_error
from .telemetry_storage import telemetry_storage
try:
    from AT.neo4j_queries import query_functions as neo4j_q
except Exception:  # neo4j optional
    neo4j_q = None
from .biosim_client import BioSimClient
from .cdra_sim_adapter import run_cdra_simulation, resample_series, anomaly_to_failure_config


def _get_physics_simulation_config() -> str:
    """Get the current physics simulation mode from Django settings."""
    from django.conf import settings
    return settings.PHYSICS_SIMULATION_MODE


def load_npy_telemetry_data(anomaly_name: str, target_sensor: str) -> List[float]:
    """
    Load telemetry data from npy files to supplement missing historical data.
    
    Args:
        anomaly_name: Name of the anomaly to load data for
        target_sensor: Target sensor name (used to determine which npy file to load)
        
    Returns:
        List of telemetry values from the npy file, or empty list if file not found
    """
    try:
        # Try to find the npy file in the parent directory (daphne_brain/)
        npy_filename = f"raw_series_{anomaly_name}.npy"
        npy_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), npy_filename)
        
        if os.path.exists(npy_path):
            print(f"📁 Physics Diagnosis: Loading npy data from {npy_path}")
            npy_data = np.load(npy_path)
            data_list = npy_data.tolist() if hasattr(npy_data, 'tolist') else list(npy_data)
            print(f"✅ Physics Diagnosis: Loaded {len(data_list)} values from npy file for '{anomaly_name}'")
            return data_list
        else:
            print(f"⚠️ Physics Diagnosis: Npy file not found at {npy_path}")
            return []
    except Exception as e:
        print(f"❌ Physics Diagnosis: Error loading npy file for '{anomaly_name}': {e}")
        return []


# Hardcoded anomaly file for supplementation - change this to use a different .npy file if needed
#SUPPLEMENTATION_ANOMALY = 'CO₂ Scrubber Valve Leak'
#SUPPLEMENTATION_ANOMALY = None
SUPPLEMENTATION_ANOMALY = 'Heater Coil Failure'



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


def _generate_simulation_time_labels(sim_duration_seconds: int, target_points: int, simulation_speed_factor: int) -> List[str]:
    """
    Generate time labels that reflect simulation time progression, accounting for simulation speed factor.
    
    Args:
        sim_duration_seconds: Total simulation duration in seconds
        target_points: Number of target data points
        simulation_speed_factor: Factor by which simulation is accelerated (e.g., 50 means 50x faster)
        
    Returns:
        List of time labels representing simulation time progression
    """
    if target_points <= 0:
        return []
    
    if sim_duration_seconds <= 0:
        return ["00:00:00"] * target_points
    
    time_labels = []
    for i in range(target_points):
        # Calculate simulation time for this point
        # Each point represents a fraction of the total simulation duration
        if target_points == 1:
            sim_time_seconds = 0
        else:
            sim_time_seconds = (i / (target_points - 1)) * sim_duration_seconds
        
        # Convert to HH:MM:SS format
        hours = int(sim_time_seconds // 3600)
        minutes = int((sim_time_seconds % 3600) // 60)
        seconds = int(sim_time_seconds % 60)
        
        time_labels.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    return time_labels


def _resample_labels(labels: List[str], target_len: int) -> List[str]:
    if not labels or target_len <= 0:
        return []
    if len(labels) == target_len:
        return list(labels)
    
    # Handle case where target length is larger than input length
    if target_len > len(labels):
        if len(labels) == 1:
            # If only one label, repeat it
            return [labels[0]] * target_len
        else:
            # Interpolate between existing labels to increase density across the full span
            result = []
            for i in range(target_len):
                # Map target index to original labels range
                # This ensures we cover the full span from first to last label
                pos = i * (len(labels) - 1) / (target_len - 1)
                idx = int(round(pos))
                result.append(labels[idx])
            
            return result
    
    # Original case: target length is smaller than or equal to input length
    result: List[str] = []
    for i in range(target_len):
        pos = i * (len(labels) - 1) / (target_len - 1)
        idx = int(round(pos))
        result.append(labels[idx])
    return result


def _normalize_series(values: List[float], baseline_min: float = None, baseline_max: float = None) -> List[float]:
    """
    Normalize a time series using either provided baseline values or the series' own min/max.
    
    Args:
        values: List of values to normalize
        baseline_min: Optional baseline minimum value for consistent normalization
        baseline_max: Optional baseline maximum value for consistent normalization
        
    Returns:
        Normalized values in range [0, 1] if using baseline, or relative to series own range
    """
    try:
        nums = [float(v) for v in values]
    except Exception:
        nums = [0.0 for _ in values]
    if not nums:
        return nums
    
    # If baseline values are provided, use them for consistent normalization
    if baseline_min is not None and baseline_max is not None:
        if baseline_max - baseline_min == 0:
            return [0.0 for _ in nums]
        return [(v - baseline_min) / (baseline_max - baseline_min) for v in nums]
    
    # Otherwise, normalize using the series' own min/max (legacy behavior)
    vmin = min(nums)
    vmax = max(nums)
    if vmax - vmin == 0:
        return [0.0 for _ in nums]
    return [(v - vmin) / (vmax - vmin) for v in nums]


def _get_unified_baseline(actual_telemetry: List[float], all_simulations: List[List[float]]) -> tuple[float, float]:
    """
    Calculate a unified baseline for normalization that encompasses both actual telemetry
    and all simulation data to ensure fair comparison.
    
    Args:
        actual_telemetry: List of actual telemetry values
        all_simulations: List of simulation value lists
        
    Returns:
        Tuple of (baseline_min, baseline_max) for unified normalization
    """
    all_values = []
    
    # Add actual telemetry values
    if actual_telemetry:
        all_values.extend(actual_telemetry)
    
    # Add all simulation values
    for sim_vals in all_simulations:
        if sim_vals:
            all_values.extend(sim_vals)
    
    if not all_values:
        return 0.0, 1.0
    
    baseline_min = min(all_values)
    baseline_max = max(all_values)
    
    # Ensure we don't have a zero range
    if baseline_max - baseline_min == 0:
        baseline_max = baseline_min + 1.0
    
    return baseline_min, baseline_max


def generate_physics_diagnosis_data(
    symptoms_list: List[Dict[str, Any]],
    target_telemetry_sensor: str,
    sim_duration_seconds: int,
    sampling_rate_seconds: int,
) -> Dict[str, Any]:
    """
    Generate physics-based diagnosis data based on symptoms.
    
    This function implements a time shift sweep approach to mitigate the uncertainty
    about when faults are injected during simulation. For each anomaly scenario,
    it sweeps through possible time alignments between simulated and actual telemetry
    to find the best match (lowest MSE), providing more robust similarity assessment.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        target_telemetry_sensor: Target telemetry sensor to analyze (default: 'ppCO2')
        
    Returns:
        Dictionary containing physics diagnosis data with anomalies, telemetry, and time labels
    """
    # simulation speed assumption:
    simulation_speed_factor = 50
    # Get real telemetry data from storage for the target sensor
    telemetry_data = get_actual_telemetry_from_storage(target_telemetry_sensor, int(sim_duration_seconds // simulation_speed_factor))
    actual_telemetry = telemetry_data['values']
    timestamps = telemetry_data['timestamps']
    unit = telemetry_data['unit']
    sensor_info = telemetry_data['sensor_info']
    
    # Determine target points from duration and sampling rate
    target_points = max(1, int(sim_duration_seconds // max(1, int(sampling_rate_seconds))))
    
    # Generate simulation-aware time labels that reflect the simulation timeline
    # These labels represent simulation time progression, not real-time telemetry collection
    time_labels = _generate_simulation_time_labels(sim_duration_seconds, target_points, simulation_speed_factor)
    
    # Resample actual series to target_points
    effective_len = target_points
    print(f"[PHYS_DIAG] Sampling plan: duration={sim_duration_seconds}s, sample_every={sampling_rate_seconds}s -> target_points={target_points}")
    print(f"[PHYS_DIAG] Simulation speed factor: {simulation_speed_factor}x")
    print(f"[PHYS_DIAG] Time labels represent simulation time (not real-time telemetry collection)")
    actual_telemetry = resample_series(actual_telemetry, target_points)
    print(f"[PHYS_DIAG] Time labels: {time_labels}")
    print(f"[PHYS_DIAG] Time labels length: {len(time_labels)}")
    print(f"[PHYS_DIAG] First label: {time_labels[0]} (simulation start)")
    print(f"[PHYS_DIAG] Last label: {time_labels[-1]} (simulation end)")
    
    
    # Generate physics-based diagnosis data
    # This simulates the physics-based analysis that would be done by the backend
    # Choose anomalies (from Neo4j if available)
    cdra_anoms = get_cdra_component_anomalies_from_neo4j(max_items=5)
    print(f"[PHYS_DIAG] Using {len(cdra_anoms)} anomalies; effective_len={effective_len}")
    print(f"[PHYS_DIAG] Anomaly names: {cdra_anoms}")
    if _get_physics_simulation_config() == 'biosim':
        target_telemetry_sensor="ppCO2_IHab"
    
    # First pass: collect all simulation data to establish unified baseline
    all_simulations = []
    for name in cdra_anoms:
        sim_vals = generate_anomaly_telemetry(
            name,
            score=0.9,  # severity seed; real severity is captured by similarity metric below
            # target_sensor='ppCO2_IHab (IHab)',
            target_sensor=target_telemetry_sensor,
            duration_seconds=int(sim_duration_seconds),
            target_len_override=effective_len,
        )['values']
        all_simulations.append(sim_vals)
        print(f"[PHYS_DIAG] Generated {len(sim_vals)} simulation values for '{name}', sim_duration={sim_duration_seconds/10}s")
    
    # Calculate unified baseline for consistent normalization
    baseline_min, baseline_max = _get_unified_baseline(actual_telemetry, all_simulations)
    print(f"[PHYS_DIAG] Unified baseline: min={baseline_min:.4f}, max={baseline_max:.4f}")
    
    # Normalize actual telemetry using unified baseline
    actual_norm = _normalize_series(actual_telemetry, baseline_min, baseline_max)
    print(f"[PHYS_DIAG] Normalized actual telemetry using unified baseline")
    print(f"[PHYS_DIAG] Actual telemetry range: raw=[{min(actual_telemetry):.4f}, {max(actual_telemetry):.4f}], normalized=[{min(actual_norm):.4f}, {max(actual_norm):.4f}]")
    print(f"[PHYS_DIAG] Actual telemetry length: {len(actual_telemetry)} -> normalized: {len(actual_norm)}")
    print(f"[PHYS_DIAG] Sampling rate: {sampling_rate_seconds}s")
    print(f"[PHYS_DIAG] Effective length: {effective_len}")
    
    # Second pass: process each anomaly with unified normalization
    comp_list = []
    for i, (name, sim_vals) in enumerate(zip(cdra_anoms, all_simulations)):
        print(f"\n[PHYS_DIAG] === Processing anomaly {i+1}/{len(cdra_anoms)}: '{name}' ===")
        print(f"[PHYS_DIAG] First 10 values: {sim_vals[:10]}")
        print(f"[PHYS_DIAG] Last 10 values: {sim_vals[-10:] if len(sim_vals) >= 10 else sim_vals}")
        
        # Normalize simulation data using the same unified baseline
        sim_norm = _normalize_series(sim_vals, baseline_min, baseline_max)
        print(f"[PHYS_DIAG] Simulation '{name}' range: raw=[{min(sim_vals):.4f}, {max(sim_vals):.4f}], normalized=[{min(sim_norm):.4f}, {max(sim_norm):.4f}]")
        print(f"[PHYS_DIAG] Simulation '{name}' length: {len(sim_vals)} -> normalized: {len(sim_norm)}")
        
        # Time shift sweep to find optimal alignment and mitigate time shift problem
        # Since fault injection timing is unclear, we sweep through possible time shifts
        # to find the best match between simulated anomaly data and actual telemetry
        # This provides a more robust similarity assessment by considering all possible alignments
        print(f"[PHYS_DIAG] === Starting time shift sweep for '{name}' ===")
        print(f"[PHYS_DIAG] actual_norm length: {len(actual_norm) if actual_norm else 'None'}")
        print(f"[PHYS_DIAG] sim_norm length: {len(sim_norm) if sim_norm else 'None'}")
        print(f"[PHYS_DIAG] Can perform shift sweep: {actual_norm and sim_norm and len(actual_norm) >= len(sim_norm)}")
        
        best_mse = float("inf")
        best_shift = 0
        best_similarity = 0.0
        
        if actual_norm and sim_norm:
            # Sweep through possible time shifts to find the best alignment
            segment_length = int(len(actual_norm)/2)
            print(f"[PHYS_DIAG] Max possible shifts: {segment_length}")
            print(f"[PHYS_DIAG] Actual telemetry range: [{min(actual_norm):.4f}, {max(actual_norm):.4f}]")
            print(f"[PHYS_DIAG] Simulation range: [{min(sim_norm):.4f}, {max(sim_norm):.4f}]")
            
            # Show first few values for debugging
            print(f"[PHYS_DIAG] First 5 actual values: {actual_norm[:5]}")
            print(f"[PHYS_DIAG] First 5 simulation values: {sim_norm[:5]}")
            
            shift_results = []
            for shift in range(len(actual_norm) - segment_length + 1):
                obs_segment = actual_norm[shift:shift + segment_length]
                hypo_segment = sim_norm[:segment_length]
                mse_score = mean_squared_error(obs_segment, hypo_segment)
                shift_results.append((shift, mse_score))
                
                if mse_score < best_mse:
                    best_mse = mse_score
                    best_shift = shift
                    best_similarity = max(0.0, min(1.0, 1.0 - mse_score * 10)) # scale down mse_score to make it more sensitive
                    print(f"[PHYS_DIAG] New best at shift {shift}: MSE={mse_score:.6f}")
            
            print(f"[PHYS_DIAG] === Shift sweep results for '{name}' ===")
            print(f"[PHYS_DIAG] All shift results (shift, MSE): {shift_results[:10]}...")  # Show first 10
            print(f"[PHYS_DIAG] Final result: best_mse={best_mse:.6f}, best_shift={best_shift}, similarity={best_similarity:.3f}")
            
        else:
            # Fallback to direct comparison if lengths don't match
            print(f"[PHYS_DIAG] === Fallback comparison for '{name}' ===")
            if actual_norm and sim_norm and len(actual_norm) == len(sim_norm):
                best_mse = mean_squared_error(actual_norm, sim_norm)
                print(f"[PHYS_DIAG] Direct comparison (same length): MSE={best_mse:.6f}")
            else:
                best_mse = 1.0
                print(f"[PHYS_DIAG] Fallback to default MSE=1.0 (lengths don't match)")
            best_shift = 0
            best_similarity = max(0.0, min(1.0, 1.0 - best_mse))
            print(f"[PHYS_DIAG] Fallback result: mse={best_mse:.6f}, similarity={best_similarity:.3f}")
        
        print(f"[PHYS_DIAG] === Final values for '{name}' ===")
        print(f"[PHYS_DIAG] best_shift: {best_shift}")
        print(f"[PHYS_DIAG] fault_injection_time: {best_shift}")
        print(f"[PHYS_DIAG] fault_injection_time_seconds: {best_shift * sampling_rate_seconds}")
        print(f"[PHYS_DIAG] ==========================================")
        
        comp_list.append({
            'name': name,
            'score': f"{best_similarity:.3f}",
            'is_highlighted': False,  # set after sorting
            'telemetry_data': sim_vals,
            'best_shift': best_shift,  # Store the best shift for debugging/analysis
            'best_mse': f"{best_mse:.4f}",  # Store the best MSE for debugging/analysis
            'fault_injection_time': best_shift,  # Time point when fault was injected (in data points)
            'fault_injection_time_seconds': best_shift * sampling_rate_seconds,  # Time in seconds
        })
        print(f"[PHYS_DIAG] === Completed anomaly {i+1}: '{name}' ===")
        print(f"[PHYS_DIAG] Added to comp_list: fault_injection_time={best_shift}, fault_injection_time_seconds={best_shift * sampling_rate_seconds}")
        print(f"[PHYS_DIAG] ==========================================\n")

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
    
    print(f"[PHYS_DIAG] === FINAL DATA STRUCTURE ===")
    print(f"[PHYS_DIAG] Component anomalies count: {len(comp_list)}")
    for i, comp in enumerate(comp_list):
        print(f"[PHYS_DIAG] Anomaly {i+1}: '{comp['name']}'")
        print(f"[PHYS_DIAG]   - fault_injection_time: {comp.get('fault_injection_time', 'MISSING')}")
        print(f"[PHYS_DIAG]   - fault_injection_time_seconds: {comp.get('fault_injection_time_seconds', 'MISSING')}")
        print(f"[PHYS_DIAG]   - best_shift: {comp.get('best_shift', 'MISSING')}")
    print(f"[PHYS_DIAG] =================================")
    
    return physics_diagnosis_data


def get_actual_telemetry_from_storage(target_sensor: str, sim_duration_seconds: int) -> Dict[str, Any]:
    """
    Get actual telemetry data from the storage system for a specific sensor.
    
    Args:
        target_sensor: Target sensor to extract telemetry data for (default: 'ppCO2')
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
        # Use seconds directly instead of converting to minutes
        time_window_seconds = max(1, sim_duration_seconds)  # Ensure at least 1 second
        
        # Get telemetry data within the specified time window
        # Try BioSim first (as it uses native parameter names), then fall back to Hera
        print(f"📊 Physics Diagnosis: Querying telemetry storage for BioSim source first, time window: {time_window_seconds} seconds")
        recent_telemetry = telemetry_storage.get_telemetry_for_physics_diagnosis(source='BioSim', time_window_seconds=time_window_seconds)
        data_source = 'BioSim'
        
        if not recent_telemetry:
            print(f"📊 Physics Diagnosis: No BioSim data found, trying Hera source")
            recent_telemetry = telemetry_storage.get_telemetry_for_physics_diagnosis(source='Hera', time_window_seconds=time_window_seconds)
            data_source = 'Hera'
        else:
            print(f"✅ Physics Diagnosis: Found {len(recent_telemetry)} BioSim telemetry records")
        
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
                
                # If we don't have enough data, try to supplement with npy file data
                if len(telemetry_values) < target_data_points:
                    print(f"⚠️ Physics Diagnosis: Insufficient data ({len(telemetry_values)} points), need {target_data_points} points")
                    
                    # Try to get supplementation data from npy files
                    # SUPPLEMENTATION_METHOD = 'npy'
                    SUPPLEMENTATION_METHOD = 'oldest_value'
                    # SUPPLEMENTATION_METHOD = 'blank_data'
                    
                    if SUPPLEMENTATION_METHOD == 'npy':
                        npy_supplementation = load_npy_telemetry_data(SUPPLEMENTATION_ANOMALY, target_sensor)
                        print(f"🔄 Physics Diagnosis: Using npy file data from '{SUPPLEMENTATION_ANOMALY}' for supplementation")
                        
                        # Calculate how many points we need to add
                        points_to_add = target_data_points - len(telemetry_values)
                        
                        # Take the most recent points from the npy data (tail end) to supplement the beginning
                        # This maintains chronological order: [npy_supplementation_data] + [actual_historical_data]
                        if len(npy_supplementation) >= points_to_add:
                            supplementation_data = npy_supplementation[-points_to_add:]  # Take tail end
                            print(f"✅ Physics Diagnosis: Using {len(supplementation_data)} points from npy file for supplementation")
                        else:
                            # If npy file doesn't have enough data, use what we have and fill the rest with oldest value
                            supplementation_data = npy_supplementation
                            remaining_points = points_to_add - len(supplementation_data)
                            oldest_value = telemetry_values[0] if telemetry_values else 0
                            supplementation_data = [oldest_value] * remaining_points + supplementation_data
                            print(f"⚠️ Physics Diagnosis: Npy file insufficient, using {len(npy_supplementation)} npy points + {remaining_points} oldest values")
                        
                        # Combine supplementation data with actual telemetry
                        telemetry_values = supplementation_data + telemetry_values
                        print(f"✅ Physics Diagnosis: Extended data to {len(telemetry_values)} points using npy supplementation")
                    elif SUPPLEMENTATION_METHOD == 'oldest_value':
                        # Fallback to old method: fill with the oldest available value
                        print(f"🔄 Physics Diagnosis: Npy supplementation failed, falling back to oldest value method")
                        
                        # Get the oldest value (first in the list since data is ordered by timestamp)
                        oldest_value = telemetry_values[0] if telemetry_values else 0
                        
                        # Calculate how many points we need to add
                        points_to_add = target_data_points - len(telemetry_values)
                        
                        # Add the oldest value to the beginning of the series (head)
                        # This maintains chronological order: [oldest_filled_data] + [actual_historical_data]
                        telemetry_values = [oldest_value] * points_to_add + telemetry_values
                        
                        print(f"✅ Physics Diagnosis: Extended data to {len(telemetry_values)} points by adding {points_to_add} oldest values ({oldest_value}) to the beginning")
                    elif SUPPLEMENTATION_METHOD == 'blank_data':
                        # Supplement None data
                        print(f"🔄 Physics Diagnosis: Filling with blank data, not even 0")

                        # Calculate how many points we need to add
                        points_to_add = target_data_points - len(telemetry_values)
                        
                        # Add the oldest value to the beginning of the series (head)
                        # This maintains chronological order: [oldest_filled_data] + [actual_historical_data]
                        telemetry_values = [None] * points_to_add + telemetry_values
                        
                    else:
                        print(f"❌ Physics Diagnosis: Invalid supplementation method: {SUPPLEMENTATION_METHOD}")
                        raise ValueError(f"Invalid supplementation method: {SUPPLEMENTATION_METHOD}")
                
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
                                print(f"✅ Physics Diagnosis: Generated {len(filled_timestamps)} timestamps for filled data")
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


def generate_anomaly_telemetry(anomaly_name: str, score: float, target_sensor: str,
                               duration_seconds: int, target_len_override: int) -> Dict[str, Any]:
    """
    Generate telemetry data using BioSim or local CDRA simulation based on configuration.
    
    Configuration is controlled by the PHYSICS_SIMULATION_MODE environment variable:
    - "biosim": Use BioSim server (default), fallback to local CDRA if unavailable
    - "local": Use local CDRA simulation only, skip BioSim entirely
    
    Examples:
        # Use BioSim with fallback to local CDRA (default)
        export PHYSICS_SIMULATION_MODE=biosim
        
        # Use local CDRA simulation only
        export PHYSICS_SIMULATION_MODE=local
    
    Args:
        anomaly_name: Name of the anomaly to simulate
        score: Severity score for the anomaly
        target_sensor: Target sensor name
        duration_seconds: Simulation duration in seconds
        target_len_override: Target length for resampling
        
    Returns:
        Dictionary containing simulation values, source type, and metadata
    """
    print(f"[ANOMALY_TELEMETRY] Generating telemetry for anomaly: '{anomaly_name}'")
    print(f"[ANOMALY_TELEMETRY] Target sensor: {target_sensor}, Duration: {duration_seconds}s, Target length: {target_len_override}")
    
    # Check simulation mode configuration
    simulation_mode = _get_physics_simulation_config()
    print(f"[ANOMALY_TELEMETRY] 🔧 Physics simulation mode: {simulation_mode}")
    
    # If local mode is explicitly set, skip BioSim entirely
    if simulation_mode == 'local':
        print(f"[ANOMALY_TELEMETRY] 🏠 Using local CDRA simulation (mode: {simulation_mode})")
        return _fallback_cdra_simulation(anomaly_name, score, target_sensor, duration_seconds, target_len_override)
    
    # Try BioSim first (only if biosim mode is enabled)
    try:
        print(f"[ANOMALY_TELEMETRY] 🔄 Attempting to use BioSim for anomaly simulation...")
        
        # Initialize BioSim client
        biosim_client = BioSimClient()
        print(f"[ANOMALY_TELEMETRY] 🚀 BioSim client initialized")
        
        # Check if BioSim server is accessible
        print(f"[ANOMALY_TELEMETRY] 🏥 Checking BioSim server status...")
        if not biosim_client.check_server_status():
            print(f"[ANOMALY_TELEMETRY] ⚠️ BioSim server is not accessible")
            print(f"[ANOMALY_TELEMETRY] 🔄 Falling back to CDRA simulation")
            return _fallback_cdra_simulation(anomaly_name, score, target_sensor, duration_seconds, target_len_override)
        
        print(f"[ANOMALY_TELEMETRY] ✅ BioSim server is accessible")
        
        # Start a NEW BioSim simulation for this specific anomaly
        print(f"[ANOMALY_TELEMETRY] 🔄 Starting new BioSim simulation for anomaly: '{anomaly_name}'")
        
        # Create anomaly-specific configuration
        # For now, we'll use a base configuration and modify it for the anomaly
        # In the future, this could be enhanced with specific fault configurations
        config_file_path = biosim_client._create_anomaly_config(anomaly_name, duration_seconds)
        
        if not config_file_path:
            print(f"[ANOMALY_TELEMETRY] ⚠️ Could not create anomaly configuration")
            print(f"[ANOMALY_TELEMETRY] 🔄 Falling back to CDRA simulation")
            return _fallback_cdra_simulation(anomaly_name, score, target_sensor, duration_seconds, target_len_override)
        
        print(f"[ANOMALY_TELEMETRY] 📄 Created anomaly configuration: {config_file_path}")
        
        # Start the new simulation
        sim_id = biosim_client.start_simulation(config_file_path)
        
        if not sim_id:
            print(f"[ANOMALY_TELEMETRY] ⚠️ Failed to start BioSim simulation")
            print(f"[ANOMALY_TELEMETRY] 🔄 Falling back to CDRA simulation")
            return _fallback_cdra_simulation(anomaly_name, score, target_sensor, duration_seconds, target_len_override)
        
        print(f"[ANOMALY_TELEMETRY] ✅ Successfully started BioSim simulation with ID: {sim_id}")
        
        # Wait a moment for simulation to run and generate data
        print(f"[ANOMALY_TELEMETRY] ⏳ Waiting for simulation to generate data...")
        import time
        time.sleep(2)  # Give simulation time to run
        
        # Now get the sensor data from this specific simulation
        print(f"[ANOMALY_TELEMETRY] 🔍 Retrieving data from simulation ID: {sim_id}")
        
        # CURRENT CODE: Using basic sensor data extraction
        # sensor_data = biosim_client.get_sensor_data_from_log(
        #     sim_id=sim_id,
        #     sensor_name=target_sensor,
        #     duration_seconds=duration_seconds
        # )
        
        # STEP 2: Replace with unit-aware sensor data extraction (commented out for now)
        sensor_data_result = biosim_client.get_sensor_data_with_units(
            sim_id=sim_id,
            sensor_name=target_sensor,
            duration_seconds=duration_seconds,
            target_unit='mmHg'  # Convert to mmHg for consistency with CDRA simulation
        )
        
        if sensor_data_result:
            sensor_data = sensor_data_result['values']
            original_unit = sensor_data_result['source_unit']
            conversion_applied = sensor_data_result['conversion_applied']
            
            if conversion_applied:
                print(f"[ANOMALY_TELEMETRY] ✅ Converted {len(sensor_data)} values from {original_unit} to mmHg")
                print(f"[ANOMALY_TELEMETRY] 📊 Conversion details: {sensor_data_result['target_unit']}")
            else:
                print(f"[ANOMALY_TELEMETRY] ℹ️ No unit conversion needed (already in {original_unit})")
        else:
            sensor_data = None
        
        if sensor_data and len(sensor_data) > 0:
            print(f"[ANOMALY_TELEMETRY] ✅ Successfully retrieved {len(sensor_data)} data points from BioSim")
            print(f"[ANOMALY_TELEMETRY] 📊 BioSim data range: [{min(sensor_data):.4f}, {max(sensor_data):.4f}]")
            
            # Resample if needed
            if target_len_override and len(sensor_data) != target_len_override:
                original_length = len(sensor_data)
                sensor_data = resample_series(sensor_data, target_len_override)
                print(f"[ANOMALY_TELEMETRY] 🔧 Resampled BioSim data from {original_length} to {len(sensor_data)} points")
            
            # Clean up temporary configuration file
            biosim_client.cleanup_temp_config(config_file_path)
            
            return {
                'values': sensor_data,
                'source': 'biosim',
                'simulation_id': sim_id,
                'anomaly_name': anomaly_name
            }
        else:
            print(f"[ANOMALY_TELEMETRY] ⚠️ No BioSim data available for sensor '{target_sensor}'")
            print(f"[ANOMALY_TELEMETRY] 🔄 Falling back to CDRA simulation")
            
            # Clean up temporary configuration file before fallback
            biosim_client.cleanup_temp_config(config_file_path)
            
            return _fallback_cdra_simulation(anomaly_name, score, target_sensor, duration_seconds, target_len_override)
            
    except Exception as e:
        print(f"[ANOMALY_TELEMETRY] ❌ Error using BioSim: {e}")
        print(f"[ANOMALY_TELEMETRY] 🔄 Falling back to CDRA simulation")
        return _fallback_cdra_simulation(anomaly_name, score, target_sensor, duration_seconds, target_len_override)


def _fallback_cdra_simulation(anomaly_name: str, score: float, target_sensor: str,
                              duration_seconds: int, target_len_override: int) -> Dict[str, Any]:
    """Local CDRA simulation - used as fallback when BioSim fails or when local mode is configured."""
    print(f"[ANOMALY_TELEMETRY] 🏠 Using local CDRA simulation for '{anomaly_name}'")
    
    # Original CDRA simulation code
    failure_cfg = anomaly_to_failure_config(anomaly_name, severity=float(score))
    baseline = 3.0
    print(f"[ANOMALY_TELEMETRY] 🔧 CDRA: Using baseline CO2: {baseline} mmHg")
    
    print(f"[ANOMALY_TELEMETRY] 🔄 CDRA: Starting simulation...")
    raw_series = run_cdra_simulation(
        failure_config=failure_cfg,
        duration_seconds=duration_seconds,
        baseline_co2_mmHg=baseline,
        onset_time_sec=3,
    )
    print(f"[ANOMALY_TELEMETRY] ✅ CDRA: Simulation completed, generated {len(raw_series)} points")
    
    if target_len_override:
        resampled = resample_series(raw_series, target_len_override)
        print(f"[ANOMALY_TELEMETRY] 🔧 CDRA: Resampled to {len(resampled)} points")
    else:
        resampled = raw_series
    
    # Determine if this is fallback or intentional local mode
    simulation_mode= _get_physics_simulation_config()
    source_type = 'cdra_local' if simulation_mode == 'local' else 'cdra_fallback'
    
    return {
        'values': resampled,
        'source': source_type,
        'anomaly_name': anomaly_name
    }


def create_physics_diagnosis_report(
    symptoms_list: List[Dict[str, Any]],
    target_telemetry_sensor: str,
    sim_duration_seconds: int,
    sampling_rate_seconds: int,
) -> Dict[str, Any]:
    """
    Create a complete physics diagnosis report.
    
    Args:
        symptoms_list: List of symptoms from the frontend
        target_telemetry_sensor: Target telemetry sensor to analyze (default: 'ppCO2')
        
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
