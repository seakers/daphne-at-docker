#!/usr/bin/env python3
"""
Test with shorter valve switching interval to show alternating bed usage
"""

import sys
import os
sys.path.append('daphne_brain')

from AT.diagnosis.physics.cdra_sim_adapter import run_cdra_simulation, anomaly_to_failure_config

def test_short_valve_interval():
    """Test with shorter valve switching interval to show alternating bed usage."""
    
    print("=" * 80)
    print("SHORT VALVE INTERVAL TEST: VALVE STUCK vs HEATER FAILURE")
    print("=" * 80)
    
    # Temporarily modify the valve switching interval for this test
    original_interval = 200
    
    test_scenarios = [
        {
            'name': 'Valve Stuck (Single Bed)',
            'anomaly': 'CO₂ Scrubber Valve Leak',
            'expected': 'Only sorbent_2 used, rapid saturation'
        },
        {
            'name': 'Heater Failure (Alternating Beds)', 
            'anomaly': 'Heater Coil Failure',
            'expected': 'Both sorbent_2 and sorbent_4 used, slower saturation'
        }
    ]
    
    results = {}
    
    for scenario in test_scenarios:
        print(f"\n{'='*60}")
        print(f"TESTING: {scenario['name']}")
        print(f"EXPECTED: {scenario['expected']}")
        print(f"{'='*60}")
        
        # Generate failure config
        failure_config = anomaly_to_failure_config(scenario['anomaly'], severity=0.9)
        
        # Run simulation with shorter valve interval by modifying the constant
        import AT.diagnosis.physics.cdra_sim_adapter as cdra
        cdra.VALVE_SWITCH_INTERVAL = 30  # Switch every 30 seconds instead of 200
        
        series = run_cdra_simulation(
            failure_config=failure_config,
            duration_seconds=120,  # 2 minutes to see multiple switches
            baseline_co2_mmHg=3.0,
            onset_time_sec=3
        )
        
        # Restore original interval
        cdra.VALVE_SWITCH_INTERVAL = original_interval
        
        results[scenario['name']] = series
        
        print(f"\nResults for '{scenario['name']}':")
        print(f"  Series length: {len(series)}")
        print(f"  Range: {min(series):.4f} to {max(series):.4f} mmHg (range: {max(series) - min(series):.4f})")
        
        # Show progression at valve switching points
        print(f"  Progression at valve switch points:")
        for t in [30, 60, 90, 119]:  # Valve switches at 30, 60, 90 seconds
            if t < len(series):
                print(f"    t={t}s: {series[t]:.4f} mmHg")
    
    # Compare results
    print(f"\n{'='*80}")
    print("COMPARISON WITH SHORT VALVE INTERVAL")
    print(f"{'='*80}")
    
    valve_series = results['Valve Stuck (Single Bed)']
    heater_series = results['Heater Failure (Alternating Beds)']
    
    print(f"\nValve Stuck (Single Bed):")
    print(f"  Final CO2: {valve_series[-1]:.4f} mmHg")
    print(f"  Change: {valve_series[-1] - valve_series[0]:.4f} mmHg")
    
    print(f"\nHeater Failure (Alternating Beds):")
    print(f"  Final CO2: {heater_series[-1]:.4f} mmHg")
    print(f"  Change: {heater_series[-1] - heater_series[0]:.4f} mmHg")
    
    # Check if they're different now
    if valve_series == heater_series:
        print("\n❌ Still identical - need to investigate further")
    else:
        print("\n✅ Different results! Confirming alternating bed theory!")
        
        # Show the differences over time
        print(f"\nTime Series Comparison:")
        print(f"Time(s) | Valve   | Heater  | Diff")
        print(f"--------|---------|---------|------")
        for t in range(30, 120, 30):
            if t < len(valve_series) and t < len(heater_series):
                diff = heater_series[t] - valve_series[t]
                print(f"{t:7d} | {valve_series[t]:7.4f} | {heater_series[t]:7.4f} | {diff:+6.4f}")

def test_valve_switching_visualization():
    """Test to visualize valve switching behavior."""
    
    print(f"\n{'='*80}")
    print("VALVE SWITCHING VISUALIZATION")
    print(f"{'='*80}")
    
    print("Testing valve switching behavior with short interval...")
    
    # Create custom configs
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
    
    heater_failure_config = {
        'filter_saturation': False,
        'filter_saturation_start': 10**9,
        'filter_saturation_end': 10**9,
        'valve_stuck': False,  # Valve continues to switch
        'valve_stuck_start': 10**9,
        'valve_stuck_end': 10**9,
        'heater_failure': ['desiccant_1', 'sorbent_2'],
        'fan_degraded': False,
        'fan_degraded_start': 10**9,
        'fan_degraded_end': 10**9,
        'degraded_flow_rate': 1.0,
    }
    
    # Modify valve interval
    import AT.diagnosis.physics.cdra_sim_adapter as cdra
    original_interval = cdra.VALVE_SWITCH_INTERVAL
    cdra.VALVE_SWITCH_INTERVAL = 20  # Switch every 20 seconds
    
    print(f"\nValve switching interval: {cdra.VALVE_SWITCH_INTERVAL} seconds")
    
    valve_series = run_cdra_simulation(
        failure_config=valve_stuck_config,
        duration_seconds=80,
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    heater_series = run_cdra_simulation(
        failure_config=heater_failure_config,
        duration_seconds=80,
        baseline_co2_mmHg=3.0,
        onset_time_sec=3
    )
    
    # Restore original interval
    cdra.VALVE_SWITCH_INTERVAL = original_interval
    
    print(f"\nResults:")
    print(f"Valve Stuck:   {[f'{x:.4f}' for x in valve_series[::20]]}")
    print(f"Heater Failure: {[f'{x:.4f}' for x in heater_series[::20]]}")
    
    if valve_series == heater_series:
        print("❌ Still identical")
    else:
        print("✅ Different! Alternating bed theory confirmed!")

if __name__ == "__main__":
    test_short_valve_interval()
    test_valve_switching_visualization()
