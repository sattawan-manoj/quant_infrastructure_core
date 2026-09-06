import numpy as np
import matplotlib.pyplot as plt

def calculate_raw_standard_deviation(vector: np.ndarray) -> float:
    """
    Calculates the Standard Deviation (sigma) from raw algebraic equations
    without using standard shortcut methods like .std() or .var().
    Uses Bessel's correction (Degrees of Freedom = n - 1) for sample variance.
    """
    n = len(vector)
    if n <= 1:
        raise ValueError("Standard deviation calculation requires at least 2 data points.")
        
    # Step 1: Calculate structural arithmetic mean
    mean_val = np.sum(vector) / n
    
    # Step 2: Compute sum of squared deviations from the mean
    squared_diff = (vector - mean_val) ** 2
    variance = np.sum(squared_diff) / (n - 1)
    
    # Step 3: Map square root step for standard deviation footprint
    return np.sqrt(variance)

def evaluate_sampling_error(population: np.ndarray, sample_size: int, num_samples: int) -> tuple:
    """
    Validates the algebraic proof of Standard Error bounds: SE = sigma / sqrt(n)
    by simulating continuous random sampling from an un-aligned population distribution.
    """
    sample_means = np.zeros(num_samples)
    
    # 1. Simulate multi-chunk independent distribution sampling
    for i in range(num_samples):
        # Continuous random sampling with replacement matrix tracking
        sample = np.random.choice(population, size=sample_size, replace=True)
        sample_means[i] = np.sum(sample) / sample_size
        
    # 2. Mathematical Proof: Algebraic derivation of theoretical Standard Error
    sigma_population = calculate_raw_standard_deviation(population)
    theoretical_se = sigma_population / np.sqrt(sample_size)
    
    # 3. Empirical Verification: Real standard deviation tracking across sample means
    empirical_se = calculate_raw_standard_deviation(sample_means)
    
    return sample_means, theoretical_se, empirical_se

if __name__ == "__main__":
    print("============= IIT-BOMBAY QUANT PROGRAMMATIC MASTERPLAN: DAY 12 =============")
    
    # Set seed parameters to lock absolute code reproducibility
    np.random.seed(42)
    
    # 1. Simulate a heavily skewed non-Gaussian population matrix (e.g., Asset Trading Volume Logs)
    print("[INFO] Generating skewed asset volume population logs (50,000 data points)...")
    population_data = np.random.exponential(scale=1000.0, size=50000)
    
    # Simulation execution parameters definition
    SAMPLE_SIZE = 100    # n = 100 tracking data matrix slices
    NUM_SAMPLES = 5000   # 5,000 independent sampling iterations
    
    # 2. Quantify error thresholds over sample mean vector arrays
    print(f"[INFO] Sampling {NUM_SAMPLES} independent chunks with sample size n={SAMPLE_SIZE}...")
    means_vector, math_se, real_se = evaluate_sampling_error(population_data, SAMPLE_SIZE, NUM_SAMPLES)
    
    # 3. Execute convergence evaluations and print mathematical verification parameters
    print("\n" + "="*65)
    print(f"📊 ALGEBRAIC PROOF VERIFICATION ENGINES:")
    print(f"-> Theoretical Standard Error (σ / √n) : {math_se:.4f}")
    print(f"-> Empirical Standard Error (Sample SD): {real_se:.4f}")
    
    # Calculate variation threshold delta (Divergence boundaries control loop)
    divergence = abs(math_se - real_se)
    print(f"-> Absolute Mathematical Divergence     : {divergence:.4f}")
    print("="*65)
    
    # Assert structural variance check to confirm production-grade logic consistency
    assert divergence < 0.5, "[CRITICAL ERROR] Empirical SE diverges significantly from Mathematical Proof!"
    print("[SUCCESS] Standard Error bounds traced cleanly and verified in millisecond domain.\n")
    
    # 4. Generate visual evaluation chart optimized for Headless Server architecture (No GUI crash)
    plt.figure(figsize=(10, 6))
    plt.hist(means_vector, bins=50, edgecolor='black', alpha=0.7, color='teal', label='Sample Means Distribution')
    plt.axvline(np.mean(means_vector), color='red', linestyle='dashed', linewidth=2, label='Grand Mean (Mean of Means)')
    plt.title(f'Sampling Distribution of Means (n={SAMPLE_SIZE})\nTheoretical SE: {math_se:.2f} | Empirical SE: {real_se:.2f}')
    plt.xlabel('Sample Mean Grid Vector Value')
    plt.ylabel('Frequency Count Density')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Save validation profile output locally instead of calling blocking .show() loops
    plt.savefig('day_12_sampling_error_bounds.png')
    print("[INFO] Visual validation profile chart safely saved as 'day_12_sampling_error_bounds.png'.")
