#!/usr/bin/env python3
"""
Test with longer duration to show valve switching effects over multiple cycles
"""

import sys
import os
sys.path.append('daphne_brain')

from AT.diagnosis.physics.cdra_sim_adapter import run_cdra_simulation, anomaly_to_failure_config

def test_long_duration():
    """Test with longer duration to show valve switching effects."""
    
    print("=" * 80)
    print("LONG DURATION TEST: VALVE STUCK vs HEATER FAILURE")
    print("Valve switching interval: 200 seconds")
    print("=" * 80)
    
    test_scenarios = [
        {
            'name': 'Valve Stuck (Single Bed)',
            'anomaly': 'CO₂ Scrubber Valve Leak',
            'description': 'Only sorbent_2 used continuously'
        },
        {
            'name': 'Heater Failure (Alternating Beds)',
            'anomaly': 'Heater Coil Failure',
            'description': 'Both sorbent_2 and sorbent_4 used alternately'
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
        
        # Run simulation with longer duration to see multiple valve switches
        print(f"\nRunning simulation for '{scenario['anomaly']}'...")
        series = run_cdra_simulation(
            failure_config=failure_config,
            duration_seconds=800,  # 4 valve switching cycles (4 * 200s)
            baseline_co2_mmHg=3.0,
            onset_time_sec=3
        )
        
        results[scenario['name']] = series
        
        print(f"\nResults for '{scenario['name']}':")
        print(f"  Series length: {len(series)}")
        print(f"  Range: {min(series):.4f} to {max(series):.4f} mmHg (range: {max(series) - min(series):.4f})")
        
        # Show progression at valve switching points (every 200s)
        print(f"  Progression at valve switch points:")
        for t in [200, 400, 600, 799]:  # Valve switches at 200, 400, 600 seconds
            if t < len(series):
                print(f"    t={t}s: {series[t]:.4f} mmHg")
    
    # Compare results
    print(f"\n{'='*80}")
    print("COMPARISON OVER LONG DURATION")
    print(f"{'='*80}")
    
    valve_data = results['Valve Stuck (Single Bed)']
    heater_data = results['Heater Failure (Alternating Beds)']
    
    valve_series = valve_data
    heater_series = heater_data
    
    print(f"\nValve Stuck (Single Bed):")
    print(f"  Final CO2 level: {valve_series[-1]:.4f} mmHg")
    print(f"  Change from start: {valve_series[-1] - valve_series[0]:.4f} mmHg")
    
    print(f"\nHeater Failure (Alternating Beds):")
    print(f"  Final CO2 level: {heater_series[-1]:.4f} mmHg")
    print(f"  Change from start: {heater_series[-1] - heater_series[0]:.4f} mmHg")
    
    # Check if they're different now
    if valve_series == heater_series:
        print("\n❌ Still producing identical results!")
        print("This suggests the fundamental issue persists even over longer duration.")
    else:
        print("\n✅ Different results! Alternating bed theory confirmed!")
        
        # Show the differences over time
        print(f"\nTime Series Comparison at valve switch points:")
        print(f"Time(s) | Valve   | Heater  | Diff")
        print(f"--------|---------|---------|------")
        for t in range(200, 800, 200):
            if t < len(valve_series) and t < len(heater_series):
                diff = heater_series[t] - valve_series[t]
                print(f"{t:7d} | {valve_series[t]:7.4f} | {heater_series[t]:7.4f} | {diff:+6.4f}")

def test_component_analysis():
    """Analyze individual component behavior."""
    
    print(f"\n{'='*80}")
    print("COMPONENT BEHAVIOR ANALYSIS")
    print(f"{'='*80}")
    
    print("Testing to understand why valve stuck and heater failure produce same results...")
    
    # Create custom configurations for detailed analysis
    valve_stuck_config = {
        'filter_saturation': False,
        'filter_saturation_start': 10**9,
        'filter_saturation_end': 10**9,
        'valve_stuck': True,
        'valve_stuck_start': 5,  # Stuck after onset
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
    
    print(f"\nRunning valve stuck simulation (600s)...")
    valve_series = run_cdra_simulation(
        failure_config=valve_stuck_config,
        duration_seconds=600,  # 3 valve switching cycles
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    print(f"\nRunning heater failure simulation (600s)...")
    heater_series = run_cdra_simulation(
        failure_config=heater_failure_config,
        duration_seconds=600,  # 3 valve switching cycles
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    print(f"\nResults:")
    print(f"Valve Stuck - Final: {valve_series[-1]:.4f} mmHg (change: {valve_series[-1] - valve_series[0]:.4f})")
    print(f"Heater Failure - Final: {heater_series[-1]:.4f} mmHg (change: {heater_series[-1] - heater_series[0]:.4f})")
    
    if valve_series == heater_series:
        print("\n❌ Still identical results!")
        print("This confirms the fundamental issue: both failures affect the same component.")
        print("The problem is that both valve stuck and heater failure ultimately")
        print("result in sorbent_2 being used without regeneration.")
    else:
        print("\n✅ Different results!")
        print("The longer duration reveals the alternating bed behavior.")

def test_different_heater_failure():
    """Test a different heater failure pattern."""
    
    print(f"\n{'='*80}")
    print("TESTING DIFFERENT HEATER FAILURE PATTERN")
    print(f"{'='*80}")
    
    # Test heater failure that affects both sorbent beds
    both_heaters_config = {
        'filter_saturation': False,
        'filter_saturation_start': 10**9,
        'filter_saturation_end': 10**9,
        'valve_stuck': False,
        'valve_stuck_start': 10**9,
        'valve_stuck_end': 10**9,
        'heater_failure': ['desiccant_1', 'sorbent_2', 'desiccant_3', 'sorbent_4'],  # All heaters fail
        'fan_degraded': False,
        'fan_degraded_start': 10**9,
        'fan_degraded_end': 10**9,
        'degraded_flow_rate': 1.0,
    }
    
    print("Testing heater failure that affects ALL heaters...")
    all_heaters_series = run_cdra_simulation(
        failure_config=both_heaters_config,
        duration_seconds=600,
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    print(f"\nResults for ALL heaters failed:")
    print(f"  Final: {all_heaters_series[-1]:.4f} mmHg")
    print(f"  Change: {all_heaters_series[-1] - all_heaters_series[0]:.4f}")
    
    # Compare with valve stuck
    valve_stuck_config = {
        'filter_saturation': False,
        'filter_saturation_start': 10**9,
        'filter_saturation_end': 10**9,
        'valve_stuck': True,
        'valve_stuck_start': 5,
        'valve_stuck_end': 10**9,
        'heater_failure': [],
        'fan_degraded': False,
        'fan_degraded_start': 10**9,
        'fan_degraded_end': 10**9,
        'degraded_flow_rate': 1.0,
    }
    
    valve_series = run_cdra_simulation(
        failure_config=valve_stuck_config,
        duration_seconds=600,
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    print(f"\nComparison:")
    print(f"Valve Stuck:     {valve_series[-1]:.4f} mmHg")
    print(f"All Heaters:     {all_heaters_series[-1]:.4f} mmHg")
    
    if valve_series == all_heaters_series:
        print("❌ Still identical!")
    else:
        print("✅ Different! This shows that affecting all heaters produces different results.")

if __name__ == "__main__":
    test_long_duration()
    test_component_analysis()
    test_different_heater_failure()
