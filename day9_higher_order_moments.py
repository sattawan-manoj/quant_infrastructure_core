"""
Day 9: High-Performance Higher-Order Moments Metrics Engine
Author: Institutional Quant Apprentice

Calculates the 3rd (Skewness) and 4th (Excess Kurtosis) statistical moments 
from scratch using pure hardware clock-speed NumPy array vectorization.
Implements rigorous runtime assertions and static type-hint structures.
"""

import numpy as np

def compute_higher_moments_core(raw_data: np.ndarray) -> tuple[float, float]:
    """
    Executes raw vectorized algebraic calculations for Skewness and Excess Kurtosis.
    Bypasses standard automated shortcuts (.mean()/.var()/.std()) entirely.
    """
    # Defensive Engineering: Input must be a valid 1D NumPy array with sufficient data footprint
    if not isinstance(raw_data, np.ndarray) or raw_data.ndim != 1:
        raise TypeError("[FATAL] Input data vector must be a 1-Dimensional NumPy array.")
    
    n: int = raw_data.shape[0]
    if n < 4:
        raise ValueError("[CRITICAL] Sample size insufficient for higher-order moments mapping.")

    # -----------------------------------------------------------------
    # NUMPY ENGINES CORE MATHEMATICAL DEPLOYMENT (NO LOOPS)
    # -----------------------------------------------------------------
    # Foundational Moment 1 & 2 Execution
    mean_val: float = float(np.sum(raw_data) / n)
    variance_val: float = float(np.sum((raw_data - mean_val) ** 2) / n)
    
    # Boundary Guard: Check for zero division (flat arrays)
    assert variance_val > 1e-12, "[SECURITY ALERT] Data variance near-zero. Calculation halted."
    std_dev: float = float(np.sqrt(variance_val))

    # Moment 3 Arithmetic: Skewness Formula (Asymmetry Index)
    deviations_cubed: np.ndarray = (raw_data - mean_val) ** 3
    calculated_skewness: float = float(np.sum(deviations_cubed) / (n * (std_dev ** 3)))

    # Moment 4 Arithmetic: Excess Kurtosis Formula (Fat-Tail Parameter Scaling)
    deviations_fourth: np.ndarray = (raw_data - mean_val) ** 4
    calculated_kurtosis: float = float((np.sum(deviations_fourth) / (n * (std_dev ** 4))) - 3.0)

    return calculated_skewness, calculated_kurtosis

if __name__ == "__main__":
    # Simulate high-volatility raw market asset returns pipeline
    np.random.seed(42)
    synthetic_returns: np.ndarray = np.random.normal(loc=0.0, scale=1.0, size=50000).astype(np.float64)
    
    # Inject synthetic tail risk shocks (simulating extreme market flash crashes)
    synthetic_returns[::100] *= 5.0  

    try:
        print("--- Initiating Hardened Day 9 Statistical Audit Engine ---")
        skew, kurtosis = compute_higher_moments_core(synthetic_returns)
        
        print(f"[METRIC COMPLETED] Calculated Skewness         : {skew:.6f}")
        print(f"[METRIC COMPLETED] Calculated Excess Kurtosis  : {kurtosis:.4f}")

        # Quantitative Risk Architecture Integration
        if kurtosis > 3.0:
            print("[RISK ALERT] Extreme Fat-Tail structure verified. Mandatory Tukey bounds required.")
        else:
            print("[TELEMETRY STATUS] Asset volatility distribution remains within normal boundaries.")
            
    except Exception as system_error:
        print(f"[EXECUTION ENGINE REJECTED] Error encountered: {system_error}")
