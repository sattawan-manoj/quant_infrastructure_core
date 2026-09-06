"""
Day 10: Institutional Multi-Variable Joint Space Analytics Engine
Author: Institutional Quant Apprentice

Deploys strict vectorized raw math to calculate Covariance and Pearson 
Correlation (ρ) across multi-asset return arrays natively.
Enforces structural input matrix dimensions locks to protect live deployment logic.
"""

import numpy as np

def execute_joint_space_mapping(vector_x: np.ndarray, vector_y: np.ndarray) -> tuple[float, float]:
    """
    Maps dynamic joint asset parameters from scratch without higher-level functional packages.
    Formula Core: Cov(X,Y) = E[(X - E[X])(Y - E[Y])] and ρ = Cov(X,Y) / (σX * σY)
    """
    # Strict Dimensional Alignment Proof (Look-ahead/Data leakage structural check)
    assert isinstance(vector_x, np.ndarray) and isinstance(vector_y, np.ndarray), "Inputs must be np.ndarray matrices."
    assert vector_x.ndim == 1 and vector_y.ndim == 1, "Data vectors must be strict 1D spaces."
    assert vector_x.shape[0] == vector_y.shape[0], "[CRITICAL TIMELINE MISMATCH] Asset vector horizons are not aligned."
    
    n: int = vector_x.shape[0]

    # -----------------------------------------------------------------
    # HARDENED VECTORIZED ARITHMETIC CORE (NO READY-MADE METHOD LOOPS)
    # -----------------------------------------------------------------
    # 1. Spatial Expectations (Mean Vectors Tracking)
    mean_x: float = float(np.sum(vector_x) / n)
    mean_y: float = float(np.sum(vector_y) / n)

    # 2. Isolated Matrix Deviations & Standard Deviation Parameters
    var_x: float = float(np.sum((vector_x - mean_x) ** 2) / n)
    var_y: float = float(np.sum((vector_y - mean_y) ** 2) / n)
    
    assert var_x > 1e-12 and var_y > 1e-12, "[CRITICAL EVALUATION FAILURE] Static vector detected. No variance variance footprint."
    std_x: float = float(np.sqrt(var_x))
    std_y: float = float(np.sqrt(var_y))

    # 3. Covariance Matrix Mapping System
    raw_covariance: float = float(np.sum((vector_x - mean_x) * (vector_y - mean_y)) / n)

    # 4. Pearson Correlation Coefficient Matrix Bounding
    raw_correlation: float = float(raw_covariance / (std_x * std_y))

    # Structural Assertion: Mathematically correlation must stay within bounds [-1.0, 1.0]
    assert -1.0001 <= raw_correlation <= 1.0001, f"[MATH VIOLATION DETECTED] Correlation out of bounds: {raw_correlation}"

    return raw_covariance, raw_correlation

if __name__ == "__main__":
    # Simulate dual core macro-asset portfolios tracking historical price lines
    asset_X_returns: np.ndarray = np.array([0.01, 0.02, -0.01, 0.03, 0.00, -0.02, 0.04, 0.01, -0.01, 0.02], dtype=np.float64)
    asset_Y_returns: np.ndarray = np.array([0.012, 0.018, -0.008, 0.025, 0.002, -0.015, 0.035, 0.008, -0.012, 0.018], dtype=np.float64)

    try:
        print("--- Initiating Hardened Day 10 Multi-Asset Joint Space Evaluation Framework ---")
        covariance, correlation = execute_joint_space_mapping(asset_X_returns, asset_Y_returns)
        
        print(f"[ENGINE STATUS CODE 200] Calculated Joint Covariance : {covariance:.6f}")
        print(f"[ENGINE STATUS CODE 200] Calculated Correlation (ρ) : {correlation:.4f}")

        # Dynamic System Screening Filter Gateway
        if correlation > 0.70:
            print("[SUCCESS FLAG] Deep linear pairing validated. Safe for statistical OLS model processing.")
        else:
            print("[WARNING] Co-movement tracking threshold breached. High decoupling risk.")

    except AssertionError as boundary_exception:
        print(f"[SECURITY SHIELD BLOCK] Validation Failed: {boundary_exception}")
