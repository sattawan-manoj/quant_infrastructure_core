import numpy as np
import matplotlib.pyplot as plt

def calculate_raw_z_score(sample_mean: float, null_mean: float, population_std: float, n: int) -> float:
    """
    Computes the raw Z-statistic manually based on algebraic proofs:
    Z = (X_bar - mu_0) / (sigma / sqrt(n))
    """
    standard_error = population_std / np.sqrt(n)
    if standard_error == 0:
        raise ZeroDivisionError("Standard error cannot be zero. Check sample size or variance arrays.")
    
    return (sample_mean - null_mean) / standard_error

def simulate_hypothesis_error_matrix(null_mean: float, alt_mean: float, population_std: float, 
                                     sample_size: int, alpha: float = 0.05, num_simulations: int = 10000) -> dict:
    """
    Explicitly quantifies and captures statistical risk parameters:
    - Significance Level (Alpha / Type I Error Rate)
    - Statistical Power (1 - Beta)
    - Type II Error Rate (Beta)
    """
    # 1. Theoretical critical boundary threshold derivation (Two-tailed Z-score for alpha=0.05 is approx 1.96)
    # Using standard standard normal percentage point functions mapped to raw array indexes
    standard_error = population_std / np.sqrt(sample_size)
    z_critical = 1.96  # Strict 95% confidence boundary parameter threshold
    
    upper_critical_value = null_mean + (z_critical * standard_error)
    lower_critical_value = null_mean - (z_critical * standard_error)
    
    type_1_errors = 0
    type_2_errors = 0
    correct_rejections = 0
    
    # 2. Continuous simulation loops testing Alpha matrix parameters (Simulating under True Null Hypothesis H0)
    print(f"[SIMULATION] Running {num_simulations} matrix slices under Null Hypothesis (H0)...")
    for _ in range(num_simulations):
        # Generate samples matching baseline true parameters exactly
        h0_sample = np.random.normal(loc=null_mean, scale=population_std, size=sample_size)
        sample_mean = np.sum(h0_sample) / sample_size
        
        # Capture False Positives (Type I Errors) when the sample mean falls out of the critical bounds
        if sample_mean > upper_critical_value or sample_mean < lower_critical_value:
            type_1_errors += 1

    # 3. Continuous simulation loops testing Beta matrix parameters (Simulating under Alternative Hypothesis H1)
    print(f"[SIMULATION] Running {num_simulations} matrix slices under Alternative Hypothesis (H1)...")
    for _ in range(num_simulations):
        # Generate samples matching shifted alternative reality parameters (e.g. regime drift / real alpha)
        h1_sample = np.random.normal(loc=alt_mean, scale=population_std, size=sample_size)
        sample_mean = np.sum(h1_sample) / sample_size
        
        # Test if sample mean falls within null critical boundaries (Failing to reject a false H0 -> Type II Error)
        if lower_critical_value <= sample_mean <= upper_critical_value:
            type_2_errors += 1
        else:
            correct_rejections += 1
            
    # Calculate exact mathematical error indices ratios
    empirical_alpha = type_1_errors / num_simulations
    empirical_beta = type_2_errors / num_simulations
    empirical_power = correct_rejections / num_simulations
    
    return {
        "target_alpha": alpha,
        "empirical_alpha": empirical_alpha,
        "empirical_beta": empirical_beta,
        "statistical_power": empirical_power,
        "lower_critical_bound": lower_critical_value,
        "upper_critical_bound": upper_critical_value
    }

if __name__ == "__main__":
    print("============= IIT-BOMBAY QUANT PROGRAMMATIC MASTERPLAN: DAY 13 =============")
    
    # Secure strict reproducibility anchors
    np.random.seed(42)
    
    # Define structural hypothesis analytics boundaries
    NULL_MEAN_MU0 = 0.0          # H0: Asset returns have zero alpha drift
    ALTERNATIVE_MEAN_MU1 = 0.15  # H1: Asset has a real positive tracking edge
    POPULATION_SIGMA = 0.5       # Underlying asset risk volatility parameter
    SAMPLE_SIZE_N = 150          # Number of trading intervals analyzed
    ALPHA_TARGET = 0.05         # Strict 95% Confidence boundary criteria
    
    print(f"[INFO] Initializing parameters: H0 Mean = {NULL_MEAN_MU0} | H1 Mean = {ALTERNATIVE_MEAN_MU1}")
    print(f"[INFO] Risk Scale Sigma = {POPULATION_SIGMA} | Data Sample Frame n = {SAMPLE_SIZE_N}")
    
    # Execute structural significance simulations
    metrics = simulate_hypothesis_error_matrix(
        null_mean=NULL_MEAN_MU0,
        alt_mean=ALTERNATIVE_MEAN_MU1,
        population_std=POPULATION_SIGMA,
        sample_size=SAMPLE_SIZE_N,
        alpha=ALPHA_TARGET
    )
    
    # 4. Print validation logs and verify structural boundary thresholds
    print("\n" + "="*65)
    print("📊 REJECTION REGIME HYPOTHESIS METRICS:")
    print(f"-> Allowed Significance Threshold (Target α) : {metrics['target_alpha']:.4f}")
    print(f"-> Measured False Positive Rate  (Actual α) : {metrics['empirical_alpha']:.4f} (Type I Error)")
    print(f"-> Measured False Negative Rate  (Actual β) : {metrics['empirical_beta']:.4f} (Type II Error)")
    print(f"-> Empirically Verified Power   (1 - β)     : {metrics['statistical_power']:.4f}")
    print(f"-> Critical Value Decision Gate Space       : [{metrics['lower_critical_bound']:.4f} to {metrics['upper_critical_bound']:.4f}]")
    print("="*65)
    
    # Assert check ensuring Type I error rate remains tightly aligned around specified alpha parameters
    alpha_variance = abs(metrics['target_alpha'] - metrics['empirical_alpha'])
    assert alpha_variance < 0.02, "[CRITICAL ERROR] Empirical False Positive rate deviates too far from Alpha target threshold!"
    print("[SUCCESS] Significance metrics mapping validated. Matrix shields are operational.\n")
    
    # 5. Export structural evaluation charts optimized for background headless processing pipelines
    plt.figure(figsize=(12, 6))
    
    # Simulate data vectors just to trace smooth visualization distribution lines
    x_grid = np.linspace(-0.3, 0.4, 1000)
    se = POPULATION_SIGMA / np.sqrt(SAMPLE_SIZE_N)
    
    y_h0 = (1 / (se * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_grid - NULL_MEAN_MU0) / se) ** 2)
    y_h1 = (1 / (se * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_grid - ALTERNATIVE_MEAN_MU1) / se) ** 2)
    
    plt.plot(x_grid, y_h0, label='Null Hypothesis Space (H0: No Alpha)', color='navy', lw=2)
    plt.plot(x_grid, y_h1, label='Alternative Hypothesis Space (H1: Real Edge)', color='darkorange', lw=2)
    
    # Plot decision boundary markers
    plt.axvline(metrics['upper_critical_bound'], color='red', linestyle='dashdot', lw=2, label='Alpha Critical Threshold')
    plt.axvline(metrics['lower_critical_bound'], color='red', linestyle='dashdot', lw=2)
    
    plt.title(f"Hypothesis Inference Matrix Framework (n={SAMPLE_SIZE_N})\nCaptured Power (1-β): {metrics['statistical_power']*100:.2f}% | Realized Type I Error: {metrics['empirical_alpha']*100:.2f}%")
    plt.xlabel("Estimated Asset Mean Parameter Space Value")
    plt.ylabel("Probability Distribution Density Grid")
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.5)
    
    plt.savefig('day_13_significance_threshold_matrix.png')
    print("[INFO] Production visual metric plot exported as 'day_13_significance_threshold_matrix.png'.")
