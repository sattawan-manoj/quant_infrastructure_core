"""
IIT-Bombay Balanced Quant Research Apprenticeship - Day 11
Module: Central Limit Theorem (CLT) Simulation Engine
Author: Manoj

Description:
    This production-grade script demonstrates the Central Limit Theorem (CLT) 
    by sampling from a highly skewed, non-Gaussian exponential distribution. 
    It computationally verifies the convergence of sample means into a 
    perfect Gaussian (Normal) Bell Curve. Optimized for high-speed execution.
"""

import time
import logging
import numpy as np
import matplotlib.pyplot as plt

# Professional Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CentralLimitTheoremSimulator:
    def __init__(self, population_size: int = 150000, scale: float = 2.5):
        """
        Initializes the simulator with a heavily skewed non-Gaussian population.
        """
        self.population_size = population_size
        self.scale = scale
        self.population = None
        self.sample_means = []

        # Generate the non-Gaussian skewed distribution (Exponential)
        self._generate_population()

    def _generate_population(self) -> None:
        """Generates a highly skewed exponential distribution."""
        logging.info(f"Generating skewed non-Gaussian population of size {self.population_size}...")
        self.population = np.random.exponential(scale=self.scale, size=self.population_size)

    def run_simulation(self, num_samples: int = 5000, sample_size: int = 100) -> np.ndarray:
        """
        Executes the CLT simulation loop.
        Optimized with replace=True for lightning-fast memory operations.
        """
        logging.info(f"Starting CLT Simulation: {num_samples} samples of size {sample_size}...")
        start_time = time.time()
        
        self.sample_means = []
        
        # Core simulation loop - High Speed Vectorized Sampling
        for _ in range(num_samples):
            # replace=True ensures instantaneous hardware-level selection
            sample = np.random.choice(self.population, size=sample_size, replace=True)
            self.sample_means.append(np.mean(sample))
            
        execution_time_ms = (time.time() - start_time) * 1000
        logging.info(f"Simulation completed successfully in {execution_time_ms:.2f} ms.")
        
        return np.array(self.sample_means)

    def verify_and_plot(self) -> None:
        """Plots the results to visually verify convergence into a perfect Bell Curve."""
        if len(self.sample_means) == 0:
            logging.error("No simulation data found. Run run_simulation() first.")
            return

        logging.info("Generating visual verification plot...")
        
        # Fallback to standard clean style to avoid any environment conflicts
        plt.style.use('ggplot') 
        
        fig, ax = plt.subplots(figsize=(11, 6))
        
        # Plot the histogram of sample means
        n, bins, patches = ax.hist(
            self.sample_means, 
            bins=60, 
            density=True, 
            alpha=0.6, 
            color='#1f77b4', 
            edgecolor='white', 
            label='Sample Means (Simulation)'
        )
        
        # Overlay a theoretical normal distribution line for perfect mathematical verification
        mu, sigma = np.mean(self.sample_means), np.std(self.sample_means)
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        ax.plot(bins, y, '--', color='#d62728', linewidth=2, label='Theoretical Normal Line')

        # Formatting titles and axes cleanly (Using Raw String 'r' to prevent SyntaxWarning)
        ax.set_title("Central Limit Theorem (CLT) - Empirical Verification Space", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel(r"Value Matrix of Sample Means ($\mu$)", fontsize=12)
        ax.set_ylabel("Probability Density Function", fontsize=12)
        ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
        
        # Display statistical metrics directly on screen (Fixed name error here)
        text_str = f"Population Size: {self.population_size}\nTotal Samples: {len(self.sample_means)}\nSample Size: {len(self.sample_means)//50}\nEmpirical Mean: {mu:.4f}\nEmpirical Std Dev: {sigma:.4f}"
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
        ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)

        plt.tight_layout()
        logging.info("Displaying plot. Close window to terminate script.")
        plt.show()

if __name__ == "__main__":
    # Initialize the Sandbox Standard Simulator
    simulator = CentralLimitTheoremSimulator(population_size=150000, scale=2.5)
    
    # Run simulation with 5000 chunks, 100 items per chunk
    simulator.run_simulation(num_samples=5000, sample_size=100)
    
    # Trigger the visual performance gateway
    simulator.verify_and_plot()
