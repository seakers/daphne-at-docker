#!/usr/bin/env python3
"""
Test script to run CDRA simulation with different anomalies
and compare the results to identify why they're producing the same values.
"""

import sys
import os
sys.path.append('daphne_brain')

from AT.diagnosis.physics.cdra_sim_adapter import run_cdra_simulation, anomaly_to_failure_config

def test_different_anomalies():
    """Test different anomaly types to see if they produce different results."""
    
    # Test anomaly names from the physics diagnosis
    test_anomalies = [
        'CO₂ Scrubber Valve Leak',
        'Fan Bearing Wear', 
        'Absorption Bed Saturated',
        'Heater Coil Failure'
    ]
    
    print("=" * 80)
    print("CDRA SIMULATION TEST - COMPARING DIFFERENT ANOMALIES")
    print("=" * 80)
    
    results = {}
    
    for anomaly_name in test_anomalies:
        print(f"\n{'='*60}")
        print(f"TESTING ANOMALY: {anomaly_name}")
        print(f"{'='*60}")
        
        # Generate failure config
        failure_config = anomaly_to_failure_config(anomaly_name, severity=0.9)
        
        # Run simulation
        print(f"\nRunning simulation for '{anomaly_name}'...")
        series = run_cdra_simulation(
            failure_config=failure_config,
            duration_seconds=100,  # Short duration for testing
            baseline_co2_mmHg=3.0,
            onset_time_sec=3
        )
        
        # Store results
        results[anomaly_name] = {
            'config': failure_config,
            'series': series,
            'min': min(series),
            'max': max(series),
            'range': max(series) - min(series)
        }
        
        print(f"\nResults for '{anomaly_name}':")
        print(f"  Series length: {len(series)}")
        print(f"  Range: {min(series):.4f} to {max(series):.4f} mmHg (range: {max(series) - min(series):.4f})")
        
        # Show first 10 values
        first_10 = [f'{x:.4f}' for x in series[:10]]
        print(f"  First 10 values: {first_10}")
        
        # Show last 10 values
        if len(series) >= 10:
            last_10 = [f'{x:.4f}' for x in series[-10:]]
        else:
            last_10 = [f'{x:.4f}' for x in series]
        print(f"  Last 10 values: {last_10}")
    
    # Compare results
    print(f"\n{'='*80}")
    print("COMPARISON OF RESULTS")
    print(f"{'='*80}")
    
    # Check if all series are identical
    all_identical = True
    first_series = results[test_anomalies[0]]['series']
    
    for i, anomaly_name in enumerate(test_anomalies[1:], 1):
        current_series = results[anomaly_name]['series']
        if current_series != first_series:
            all_identical = False
            print(f"✅ Series {i} ({anomaly_name}) is DIFFERENT from first series")
        else:
            print(f"❌ Series {i} ({anomaly_name}) is IDENTICAL to first series")
    
    if all_identical:
        print(f"\n❌ ALL SERIES ARE IDENTICAL! This indicates a problem.")
    else:
        print(f"\n✅ Series are different - simulation is working correctly.")
    
    # Show detailed comparison
    print(f"\n{'='*80}")
    print("DETAILED COMPARISON")
    print(f"{'='*80}")
    
    for anomaly_name in test_anomalies:
        result = results[anomaly_name]
        print(f"\n{anomaly_name}:")
        print(f"  Config: {result['config']}")
        print(f"  Range: {result['min']:.4f} - {result['max']:.4f} (Δ={result['range']:.4f})")
        
        # Show first 5 values
        first_5 = [f'{x:.4f}' for x in result['series'][:5]]
        print(f"  First 5: {first_5}")
        
        # Show last 5 values
        if len(result['series']) >= 5:
            last_5 = [f'{x:.4f}' for x in result['series'][-5:]]
        else:
            last_5 = [f'{x:.4f}' for x in result['series']]
        print(f"  Last 5: {last_5}")

if __name__ == "__main__":
    test_different_anomalies()
