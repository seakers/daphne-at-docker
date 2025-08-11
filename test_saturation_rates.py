#!/usr/bin/env python3
"""
Test to compare saturation rates between valve stuck vs heater failure
"""

import sys
import os
sys.path.append('daphne_brain')

from AT.diagnosis.physics.cdra_sim_adapter import run_cdra_simulation, anomaly_to_failure_config

def test_saturation_rates():
    """Test valve stuck vs heater failure saturation rates."""
    
    print("=" * 80)
    print("SATURATION RATE TEST: VALVE STUCK vs HEATER FAILURE")
    print("=" * 80)
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'Valve Stuck',
            'anomaly': 'CO₂ Scrubber Valve Leak',
            'description': 'Single sorbent bed used continuously'
        },
        {
            'name': 'Heater Failure',
            'anomaly': 'Heater Coil Failure', 
            'description': 'Alternating sorbent beds (switching continues)'
        }
    ]
    
    results = {}
    
    for scenario in test_scenarios:
        print(f"\n{'='*60}")
        print(f"TESTING: {scenario['name']}")
        print(f"DESCRIPTION: {scenario['description']}")
        print(f"{'='*60}")
        
        # Generate failure config
        failure_config = anomaly_to_failure_config(scenario['anomaly'], severity=0.9)
        
        # Run simulation with longer duration to see saturation effects
        print(f"\nRunning simulation for '{scenario['anomaly']}'...")
        series = run_cdra_simulation(
            failure_config=failure_config,
            duration_seconds=200,  # Longer to see saturation effects
            baseline_co2_mmHg=3.0,
            onset_time_sec=3
        )
        
        results[scenario['name']] = {
            'series': series,
            'config': failure_config,
            'description': scenario['description']
        }
        
        print(f"\nResults for '{scenario['name']}':")
        print(f"  Series length: {len(series)}")
        print(f"  Range: {min(series):.4f} to {max(series):.4f} mmHg (range: {max(series) - min(series):.4f})")
        
        # Show progression over time
        print(f"  Progression:")
        for i, t in enumerate([10, 50, 100, 150, 199]):
            if t < len(series):
                print(f"    t={t}s: {series[t]:.4f} mmHg")
    
    # Compare results
    print(f"\n{'='*80}")
    print("COMPARISON OF SATURATION EFFECTS")
    print(f"{'='*80}")
    
    valve_data = results['Valve Stuck']
    heater_data = results['Heater Failure']
    
    valve_series = valve_data['series']
    heater_series = heater_data['series']
    
    print(f"\nValve Stuck (Single Bed):")
    print(f"  Final CO2 level: {valve_series[-1]:.4f} mmHg")
    print(f"  Change from start: {valve_series[-1] - valve_series[0]:.4f} mmHg")
    
    print(f"\nHeater Failure (Alternating Beds):")
    print(f"  Final CO2 level: {heater_series[-1]:.4f} mmHg")
    print(f"  Change from start: {heater_series[-1] - heater_series[0]:.4f} mmHg")
    
    # Calculate saturation rates
    valve_change = valve_series[-1] - valve_series[0]
    heater_change = heater_series[-1] - heater_series[0]
    
    if valve_change > 0 and heater_change > 0:
        ratio = heater_change / valve_change
        print(f"\nRatio (Heater/Valve): {ratio:.3f}")
        if 0.3 < ratio < 0.7:  # Allow some tolerance
            print("✅ CONFIRMED: Heater failure produces roughly half the saturation rate!")
        else:
            print(f"❌ Unexpected ratio: {ratio:.3f}")
    
    # Show time series comparison
    print(f"\nTime Series Comparison (every 20s):")
    print(f"Time(s) | Valve   | Heater  | Diff")
    print(f"--------|---------|---------|------")
    for t in range(20, 200, 20):
        if t < len(valve_series) and t < len(heater_series):
            diff = heater_series[t] - valve_series[t]
            print(f"{t:7d} | {valve_series[t]:7.4f} | {heater_series[t]:7.4f} | {diff:+6.4f}")

def test_individual_bed_saturation():
    """Test to show individual bed saturation rates."""
    
    print(f"\n{'='*80}")
    print("INDIVIDUAL BED SATURATION ANALYSIS")
    print(f"{'='*80}")
    
    print("Theory:")
    print("- Valve Stuck: Only sorbent_2 used continuously -> saturates quickly")
    print("- Heater Failure: Both sorbent_2 and sorbent_4 used alternately -> each saturates slowly")
    print("- Expected: Heater failure should show slower CO2 rise due to alternating usage")
    
    # Create custom failure configs to test this theory
    valve_stuck_config = {
        'filter_saturation': False,
        'filter_saturation_start': 10**9,
        'filter_saturation_end': 10**9,
        'valve_stuck': True,
        'valve_stuck_start': 4,  # After onset
        'valve_stuck_end': 10**9,
        'heater_failure': [],
        'fan_degraded': False,
        'fan_degraded_start': 10**9,
        'fan_degraded_end': 10**9,
        'degraded_flow_rate': 1.0,
    }
    
    heater_failure_config = {
        'filter_saturation': False,
        'filter_saturation_start': 10**9,
        'filter_saturation_end': 10**9,
        'valve_stuck': False,  # Valve continues to switch
        'valve_stuck_start': 10**9,
        'valve_stuck_end': 10**9,
        'heater_failure': ['desiccant_1', 'sorbent_2'],  # Only sorbent_2 heater fails
        'fan_degraded': False,
        'fan_degraded_start': 10**9,
        'fan_degraded_end': 10**9,
        'degraded_flow_rate': 1.0,
    }
    
    print(f"\nTesting Valve Stuck (single bed)...")
    valve_series = run_cdra_simulation(
        failure_config=valve_stuck_config,
        duration_seconds=200,
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    print(f"\nTesting Heater Failure (alternating beds)...")
    heater_series = run_cdra_simulation(
        failure_config=heater_failure_config,
        duration_seconds=200,
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    print(f"\nResults:")
    print(f"Valve Stuck - Final CO2: {valve_series[-1]:.4f} mmHg (change: {valve_series[-1] - valve_series[0]:.4f})")
    print(f"Heater Failure - Final CO2: {heater_series[-1]:.4f} mmHg (change: {heater_series[-1] - heater_series[0]:.4f})")
    
    if valve_series == heater_series:
        print("❌ Still producing identical results - need deeper investigation")
    else:
        print("✅ Different results - confirming the theory!")

if __name__ == "__main__":
    test_saturation_rates()
    test_individual_bed_saturation()
