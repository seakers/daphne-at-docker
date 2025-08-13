#!/usr/bin/env python3
"""
Test script to verify the time shift sweep functionality in physics diagnosis.
This script demonstrates how the new approach works to find optimal alignment
between simulated and actual telemetry data.
"""

import numpy as np
from sklearn.metrics import mean_squared_error

def test_time_shift_sweep():
    """Test the time shift sweep approach with synthetic data."""
    
    # Simulate actual telemetry data (longer series)
    np.random.seed(42)
    actual_telemetry = np.random.normal(100, 10, 50)  # 50 data points
    
    # Simulate anomaly data (shorter series, representing the fault scenario)
    anomaly_data = np.random.normal(120, 15, 20)  # 20 data points
    
    # Normalize both series
    def normalize_series(values):
        vmin, vmax = np.min(values), np.max(values)
        if vmax - vmin == 0:
            return np.zeros_like(values)
        return (values - vmin) / (vmax - vmin)
    
    actual_norm = normalize_series(actual_telemetry)
    anomaly_norm = normalize_series(anomaly_data)
    
    print("=== Time Shift Sweep Test ===")
    print(f"Actual telemetry length: {len(actual_norm)}")
    print(f"Anomaly data length: {len(anomaly_norm)}")
    print(f"Max possible shifts: {len(actual_norm) - len(anomaly_norm) + 1}")
    
    # Implement the time shift sweep
    best_mse = float("inf")
    best_shift = 0
    best_similarity = 0.0
    
    print("\n=== Sweeping through time shifts ===")
    for shift in range(len(actual_norm) - len(anomaly_norm) + 1):
        obs_segment = actual_norm[shift:shift + len(anomaly_norm)]
        hypo_segment = anomaly_norm
        mse = mean_squared_error(obs_segment, hypo_segment)
        
        print(f"Shift {shift:2d}: MSE = {mse:.6f}")
        
        if mse < best_mse:
            best_mse = mse
            best_shift = shift
            best_similarity = max(0.0, min(1.0, 1.0 - mse))
    
    print(f"\n=== Results ===")
    print(f"Best shift: {best_shift}")
    print(f"Best MSE: {best_mse:.6f}")
    print(f"Best similarity: {best_similarity:.6f}")
    
    # Compare with direct alignment (no shift)
    direct_mse = mean_squared_error(actual_norm[:len(anomaly_norm)], anomaly_norm)
    direct_similarity = max(0.0, min(1.0, 1.0 - direct_mse))
    
    print(f"\n=== Comparison ===")
    print(f"Direct alignment (no shift): MSE = {direct_mse:.6f}, Similarity = {direct_similarity:.6f}")
    print(f"Time shift sweep: MSE = {best_mse:.6f}, Similarity = {best_similarity:.6f}")
    print(f"Improvement: MSE reduced by {direct_mse - best_mse:.6f}, Similarity increased by {best_similarity - direct_similarity:.6f}")
    
    return best_shift, best_mse, best_similarity

if __name__ == "__main__":
    test_time_shift_sweep()
