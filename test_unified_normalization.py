#!/usr/bin/env python3
"""
Test script to demonstrate the difference between independent vs unified normalization.
This shows how the new unified baseline approach provides fair comparison between
actual telemetry and simulation data.
"""

import numpy as np
from sklearn.metrics import mean_squared_error

def normalize_series_independent(values):
    """Old approach: normalize each series independently using its own min/max."""
    vmin, vmax = np.min(values), np.max(values)
    if vmax - vmin == 0:
        return np.zeros_like(values)
    return (values - vmin) / (vmax - vmin)

def normalize_series_unified(values, baseline_min, baseline_max):
    """New approach: normalize using unified baseline for consistent comparison."""
    if baseline_max - baseline_min == 0:
        return np.zeros_like(values)
    return (values - baseline_min) / (baseline_max - baseline_min)

def get_unified_baseline(actual_telemetry, all_simulations):
    """Calculate unified baseline encompassing all data."""
    all_values = []
    if len(actual_telemetry) > 0:
        all_values.extend(actual_telemetry)
    for sim_vals in all_simulations:
        if len(sim_vals) > 0:
            all_values.extend(sim_vals)
    
    if not all_values:
        return 0.0, 1.0
    
    baseline_min = min(all_values)
    baseline_max = max(all_values)
    
    if baseline_max - baseline_min == 0:
        baseline_max = baseline_min + 1.0
    
    return baseline_min, baseline_max

def test_normalization_approaches():
    """Compare independent vs unified normalization approaches."""
    
    print("=== Normalization Approach Comparison ===\n")
    
    # Simulate realistic data
    np.random.seed(42)
    
    # Actual telemetry: CO2 levels around 400-500 ppm
    actual_telemetry = np.random.normal(450, 25, 30)  # 30 data points
    
    # Simulation 1: CO2 scrubber valve leak (higher CO2 levels)
    sim1_vals = np.random.normal(600, 30, 20)  # 20 data points
    
    # Simulation 2: Fan bearing wear (moderate CO2 increase)
    sim2_vals = np.random.normal(500, 20, 20)  # 20 data points
    
    print("Raw Data Ranges:")
    print(f"  Actual telemetry: [{actual_telemetry.min():.1f}, {actual_telemetry.max():.1f}]")
    print(f"  Simulation 1 (valve leak): [{sim1_vals.min():.1f}, {sim1_vals.max():.1f}]")
    print(f"  Simulation 2 (fan wear): [{sim1_vals.min():.1f}, {sim2_vals.max():.1f}]")
    
    # Approach 1: Independent normalization (OLD)
    print("\n=== Approach 1: Independent Normalization (OLD) ===")
    actual_norm_indep = normalize_series_independent(actual_telemetry)
    sim1_norm_indep = normalize_series_independent(sim1_vals)
    sim2_norm_indep = normalize_series_independent(sim2_vals)
    
    print("Normalized ranges (independent):")
    print(f"  Actual telemetry: [{actual_norm_indep.min():.4f}, {actual_norm_indep.max():.4f}]")
    print(f"  Simulation 1: [{sim1_norm_indep.min():.4f}, {sim1_norm_indep.max():.4f}]")
    print(f"  Simulation 2: [{sim2_norm_indep.min():.4f}, {sim2_norm_indep.max():.4f}]")
    
    # Calculate MSE for independent normalization
    # Note: We can only compare if lengths match, so we'll truncate
    min_len = min(len(actual_norm_indep), len(sim1_norm_indep), len(sim2_norm_indep))
    mse1_indep = mean_squared_error(actual_norm_indep[:min_len], sim1_norm_indep[:min_len])
    mse2_indep = mean_squared_error(actual_norm_indep[:min_len], sim2_norm_indep[:min_len])
    
    print(f"\nMSE with independent normalization:")
    print(f"  Simulation 1 vs Actual: {mse1_indep:.6f}")
    print(f"  Simulation 2 vs Actual: {mse2_indep:.6f}")
    
    # Approach 2: Unified normalization (NEW)
    print("\n=== Approach 2: Unified Normalization (NEW) ===")
    
    # Calculate unified baseline
    all_simulations = [sim1_vals, sim2_vals]
    baseline_min, baseline_max = get_unified_baseline(actual_telemetry, all_simulations)
    print(f"Unified baseline: [{baseline_min:.1f}, {baseline_max:.1f}]")
    
    # Normalize all data using unified baseline
    actual_norm_unified = normalize_series_unified(actual_telemetry, baseline_min, baseline_max)
    sim1_norm_unified = normalize_series_unified(sim1_vals, baseline_min, baseline_max)
    sim2_norm_unified = normalize_series_unified(sim2_vals, baseline_min, baseline_max)
    
    print("Normalized ranges (unified baseline):")
    print(f"  Actual telemetry: [{actual_norm_unified.min():.4f}, {actual_norm_unified.max():.4f}]")
    print(f"  Simulation 1: [{sim1_norm_unified.min():.4f}, {sim1_norm_unified.max():.4f}]")
    print(f"  Simulation 2: [{sim2_norm_unified.min():.4f}, {sim2_norm_unified.max():.4f}]")
    
    # Calculate MSE for unified normalization
    mse1_unified = mean_squared_error(actual_norm_unified[:min_len], sim1_norm_unified[:min_len])
    mse2_unified = mean_squared_error(actual_norm_unified[:min_len], sim2_norm_unified[:min_len])
    
    print(f"\nMSE with unified normalization:")
    print(f"  Simulation 1 vs Actual: {mse1_unified:.6f}")
    print(f"  Simulation 2 vs Actual: {mse2_unified:.6f}")
    
    # Analysis
    print("\n=== Analysis ===")
    print("Independent normalization issues:")
    print("  - Each series normalized to [0,1] independently")
    print("  - Relative scale differences are lost")
    print("  - MSE comparison becomes meaningless")
    
    print("\nUnified normalization benefits:")
    print("  - All series use same baseline reference")
    print("  - Relative scale differences are preserved")
    print("  - MSE comparison becomes meaningful")
    print("  - Fair comparison between actual and simulated data")
    
    print(f"\nMSE difference (unified - independent):")
    print(f"  Simulation 1: {mse1_unified - mse1_indep:+.6f}")
    print(f"  Simulation 2: {mse2_unified - mse2_indep:+.6f}")
    
    return {
        'independent': {'sim1': mse1_indep, 'sim2': mse2_indep},
        'unified': {'sim1': mse1_unified, 'sim2': mse2_unified}
    }

if __name__ == "__main__":
    test_normalization_approaches()
