#!/usr/bin/env python3
"""
Focused test to compare heater failure vs valve leak
"""

import sys
import os
sys.path.append('daphne_brain')

from AT.diagnosis.physics.cdra_sim_adapter import run_cdra_simulation, anomaly_to_failure_config

def test_heater_vs_valve():
    """Test heater failure vs valve leak specifically."""
    
    print("=" * 80)
    print("FOCUSED TEST: HEATER FAILURE vs VALVE LEAK")
    print("=" * 80)
    
    # Test the two problematic anomalies
    test_anomalies = [
        'CO₂ Scrubber Valve Leak',
        'Heater Coil Failure'
    ]
    
    results = {}
    
    for anomaly_name in test_anomalies:
        print(f"\n{'='*60}")
        print(f"TESTING ANOMALY: {anomaly_name}")
        print(f"{'='*60}")
        
        # Generate failure config
        failure_config = anomaly_to_failure_config(anomaly_name, severity=0.9)
        
        # Run simulation with shorter duration for clarity
        print(f"\nRunning simulation for '{anomaly_name}'...")
        series = run_cdra_simulation(
            failure_config=failure_config,
            duration_seconds=50,  # Shorter for clearer debugging
            baseline_co2_mmHg=3.0,
            onset_time_sec=3
        )
        
        results[anomaly_name] = series
        
        print(f"\nResults for '{anomaly_name}':")
        print(f"  Series length: {len(series)}")
        print(f"  Range: {min(series):.4f} to {max(series):.4f} mmHg (range: {max(series) - min(series):.4f})")
        print(f"  First 5: {[f'{x:.4f}' for x in series[:5]]}")
        print(f"  Last 5: {[f'{x:.4f}' for x in series[-5:]]}")
    
    # Compare results
    print(f"\n{'='*80}")
    print("COMPARISON")
    print(f"{'='*80}")
    
    valve_series = results['CO₂ Scrubber Valve Leak']
    heater_series = results['Heater Coil Failure']
    
    if valve_series == heater_series:
        print("❌ SERIES ARE IDENTICAL!")
        print("This confirms the issue: heater failure and valve leak produce the same effect.")
    else:
        print("✅ SERIES ARE DIFFERENT!")
    
    # Show the differences
    print(f"\nDetailed comparison:")
    print(f"Valve Leak:   {[f'{x:.4f}' for x in valve_series[-10:]]}")
    print(f"Heater Failure: {[f'{x:.4f}' for x in heater_series[-10:]]}")

if __name__ == "__main__":
    test_heater_vs_valve()
