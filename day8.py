import numpy as np

def simulate_expectation_space(steps: int = 100000) -> float:
    """
    Day 8: Random Variables & Expected Value Space
    Calculates the spatial infinity average (Mathematical Expectation E[X])
    over simulated discrete paths without utilizing short-cut methods.
    """
    try:
        print("[INIT] Executing Continuous & Discrete Random Variable Simulations...")
        
        # Simulating random variable outcomes (e.g., discrete values 1 to 6 with unequal weights)
        outcomes = np.array([1, 2, 3, 4, 5, 6], dtype=np.float64)
        probabilities = np.array([0.1, 0.15, 0.2, 0.3, 0.15, 0.1])
        
        # Verify strict probability boundary: Sum must equal 1.0
        assert np.isclose(np.sum(probabilities), 1.0), "[ERROR] Probability distribution values are non-unitary!"
        
        # Generate tracking paths across multiple independent observation chunks
        simulated_paths = np.random.choice(outcomes, size=steps, p=probabilities)
        
        # Calculate spatial average step-by-step from scratch: E[X] = Sum(x * P(x))
        unique_elements, counts = np.unique(simulated_paths, return_counts=True)
        empirical_probabilities = counts / steps
        
        expected_value = np.sum(unique_elements * empirical_probabilities)
        
        print("\n" + "="*50)
        print("📊 EXPECTED VALUE ENGINE OUTPUT (DAY 8)")
        print(f"• Sample Paths Simulated: {steps}")
        print(f"• Calculated Expectation E[X]: {expected_value:.4f}")
        print("="*50)
        
        return float(expected_value)
    except AssertionError as ae:
        print(f"[ASSERTION ERROR] Configuration breakdown: {str(ae)}")
        raise
    except Exception as e:
        print(f"[ERROR] Engine failure inside state-space matrix: {str(e)}")
        raise

if __name__ == "__main__":
    simulate_expectation_space(steps=100000)
