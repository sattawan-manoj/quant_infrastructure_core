import numpy as np

def run_expectation_simulation(num_paths: int = 10, total_steps: int = 100000):
    """
    Simulates continuous random variables across multiple paths to track 
    how the running sample mean converges toward the true theoretical expected value.
    """
    print(f"[INIT] Launching {num_paths} simulation paths with {total_steps:,} steps each...")

    # 1. Define theoretical parameters for a continuous distribution (Normal Distribution)
    # For a standard normal distribution, Theoretical Expected Value E[X] = mu
    true_mu = 0.05  # Assume a theoretical expected return of 5%
    true_sigma = 0.15 # Volatility scale

    # 2. Vectorized Generation of Random Spaces (C-contiguous blocks for clock speed)
    # We generate a massive matrix layout: Rows = Steps, Columns = Independent Paths
    print("[COMPUTING] Allocating raw memory blocks for random trajectories...")
    raw_shocks = np.random.normal(loc=true_mu, scale=true_sigma, size=(total_steps, num_paths))
    
    # 3. Calculate Cumulative Expected Value Space Step-by-Step
    # np.cumsum accumulates the values down the rows for each independent path
    cumulative_sums = np.cumsum(raw_shocks, axis=0)
    
    # Create a step-counter vector (1 to total_steps) and reshape for broadcasting
    step_counters = np.arange(1, total_steps + 1).reshape(-1, 1)
    
    # NumPy Broadcasting: Stretches the smaller step vector horizontally across all asset spaces
    # Running Mean = Cumulative Sum / Number of Steps elapsed
    running_expectations = cumulative_sums / step_counters

    # 4. Evaluate Final Convergence Metrics
    print("\n📊 --- FINAL CONVERGENCE LEDGER ---")
    print(f"Target Theoretical Expected Value E[X]: {true_mu:.6f}")
    
    for path_idx in range(min(5, num_paths)): # Display results for the first 5 paths
        final_empirical_mean = running_expectations[-1, path_idx]
        absolute_error = abs(final_empirical_mean - true_mu)
        print(f"Path {path_idx + 1} Final Sample Average: {final_empirical_mean:.6f} | Error vs E[X]: {absolute_error:.6f}")

    return running_expectations, true_mu

if __name__ == "__main__":
    # Execute the raw arithmetic arrays
    running_exp, theoretical_val = run_expectation_simulation(num_paths=5, total_steps=500000)
