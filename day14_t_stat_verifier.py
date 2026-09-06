import numpy as np
import time

def calculate_raw_moments(vector: np.ndarray) -> tuple:
    """
    Calculates sample mean and sample variance from raw arithmetic formulas
    without using shortcut wrappers like .mean() or .var().
    """
    n = len(vector)
    if n <= 1:
        raise ValueError("Matrix vector must contain at least 2 data points.")
        
    # Step 1: Calculate structural arithmetic mean
    sample_mean = np.sum(vector) / n
    
    # Step 2: Compute sample variance using Bessel's Correction (df = n - 1)
    squared_deviations = (vector - sample_mean) ** 2
    sample_variance = np.sum(squared_deviations) / (n - 1)
    
    return sample_mean, sample_variance

def execute_two_sample_t_test(vector_a: np.ndarray, vector_b: np.ndarray) -> dict:
    """
    Computes a raw Two-Sample T-test assuming unequal variances (Welch's T-test)
    completely from algebraic equations to enforce strict foundational tracking.
    """
    n1 = len(vector_a)
    n2 = len(vector_b)
    
    # Extract raw structural statistics from vectors
    mean1, var1 = calculate_raw_moments(vector_a)
    mean2, var2 = calculate_raw_moments(vector_b)
    
    # Calculate Welch-Satterthwaite pooled standard error proof
    se_pooled = np.sqrt((var1 / n1) + (var2 / n2))
    
    # Calculate the raw t-statistic
    if se_pooled == 0:
        raise ZeroDivisionError("Pooled Standard Error cannot be zero. Verify array variance.")
    t_statistic = (mean1 - mean2) / se_pooled
    
    # Approximate Welch-Satterthwaite degrees of freedom equation
    numerator = ((var1 / n1) + (var2 / n2)) ** 2
    denominator = (((var1 / n1) ** 2) / (n1 - 1)) + (((var2 / n2) ** 2) / (n2 - 1))
    degrees_of_freedom = numerator / denominator
    
    # For a strict 95% confidence boundary (alpha = 0.05, two-tailed), 
    # the large-sample critical t-value converges near 1.96.
    # We apply an asymptotic normal approximation rule for large quant footprints.
    critical_t_value = 1.96
    
    # Decision logical matrix condition
    reject_null = abs(t_statistic) > critical_t_value
    
    return {
        "mean_a": mean1,
        "mean_b": mean2,
        "t_stat": t_statistic,
        "df": degrees_of_freedom,
        "critical_t": critical_t_value,
        "reject_null_h0": reject_null
    }

if __name__ == "__main__":
    print("============= IIT-BOMBAY QUANT PROGRAMMATIC MASTERPLAN: DAY 14 =============")
    
    # Lock operational code reproducibility seeds
    np.random.seed(42)
    
    # 1. Simulating two massive trading asset return vectors (50,000 data elements each)
    # Asset A: Baseline Market Index | Asset B: Alpha Strategy Portfolio
    print("[INFO] Generating massive synthetic multi-asset histories (2 x 50,000 matrix fields)...")
    asset_returns_a = np.random.normal(loc=0.0002, scale=0.015, size=50000) # Baseline Market
    asset_returns_b = np.random.normal(loc=0.0006, scale=0.016, size=50000) # Outperforming Strategy
    
    # 2. Performance benchmark evaluation: Track execution time in millisecond domain
    print("[INFO] Passing massive arrays to verification engines via terminal runtime...")
    start_time = time.time()
    
    test_results = execute_two_sample_t_test(asset_returns_a, asset_returns_b)
    
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000
    
    # 3. Print structural verification metrics and assert runtime speed boundaries
    print("\n" + "="*70)
    print("📊 WEEK 2 FINAL PERFORMANCE BENCHMARK GATEWAY:")
    print(f"-> Asset Vector A Sample Mean       : {test_results['mean_a']:.6f}")
    print(f"-> Asset Vector B Sample Mean       : {test_results['mean_b']:.6f}")
    print(f"-> Derived Welch T-Statistic        : {test_results['t_stat']:.4f}")
    print(f"-> Welch-Satterthwaite DF Bounds   : {test_results['df']:.2f}")
    print(f"-> Alpha Decision Threshold Bound   : ±{test_results['critical_t']}")
    
    print("-" * 70)
    if test_results['reject_null_h0']:
        print("❌ STATUS: [REJECT H0] Equal mean parameters rejected at 95% Confidence Level.")
        print("   -> Implication: The strategy performance difference is STATISTICALLY SIGNIFICANT.")
    else:
        print("✅ STATUS: [FAIL TO REJECT H0] Equal mean parameters cannot be rejected.")
        print("   -> Implication: Performance variance may be caused by absolute random noise.")
    print("="*70)
    
    print(f"[BENCHMARK] Computational processing cycle resolved in: {execution_time_ms:.4f} ms")
    
    # Assert check ensuring structural execution maps inside the millisecond domain
    assert execution_time_ms < 50.0, "[PERFORMANCE CRASH] Processing cycle exceeded strict millisecond constraints!"
    print("[SUCCESS] Day 14 milestone verified. Week 2 probability foundations are unshakeable.")
