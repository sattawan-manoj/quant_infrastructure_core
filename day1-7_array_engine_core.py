import numpy as np
import time

def initialize_memory_matrix(rows: int = 500000, cols: int = 2) -> np.ndarray:
    """
    Day 1 & Day 2: Memory Allocation & Continuous Slicing
    Provisions a C-contiguous matrix in float64 for maximum hardware execution.
    Tracks simulated multi-asset histories across time intervals.
    """
    try:
        # Day 1: Initialize raw memory layout block
        raw_matrix = np.random.randn(rows, cols)
        matrix_contiguous = np.array(raw_matrix, dtype=np.float64, order='C')
        
        # Day 2: Continuous Slicing & Memory Mutation evaluation
        # Slicing the first asset history cut without copying memory
        asset_cut = matrix_contiguous[0:rows, 0:1]
        
        # Verify if it's a memory view (True) or a deep duplicate (False)
        assert asset_cut.base is matrix_contiguous, "[ERROR] Memory is duplicated instead of viewed!"
        return matrix_contiguous
    except MemoryError:
        print("[CRITICAL] System ran out of memory during matrix allocation.")
        raise

def process_vectorized_returns(matrix: np.ndarray) -> np.ndarray:
    """
    Day 3 & Day 4: Vectorization, Broadcasting & Logical Masking
    Eliminates explicit loops. Replaces anomalies using logical boolean masks.
    """
    try:
        # Day 3: Vectorized operations simulating asset alterations (log, exp, sqrt)
        # Using abs to avoid negative logs, stretching calculations across 500,000 rows
        log_transformed = np.log(np.abs(matrix) + 1e-8)
        
        # Day 4: Logical Masking & Data Cleaning
        # Condition: Zero out extreme mathematical spikes or negative values structurally
        clean_matrix = np.where(log_transformed < 0.0, 0.0, log_transformed)
        return clean_matrix
    except Exception as e:
        print(f"[ERROR] Exception hit during vectorized computation: {str(e)}")
        raise

def calculate_raw_moments(vector: np.ndarray) -> dict:
    """
    Day 5, Day 6 & Day 7: Functional Parameters, Exception Blocks & Raw Math Moments
    Calculates Mean, Variance, and Standard Deviation step-by-step WITHOUT .mean() or .var()
    """
    # Day 5: Type hinting layout enforced
    if not isinstance(vector, np.ndarray):
        raise TypeError("Input must be a valid NumPy ndarray")
        
    try:
        n = vector.shape[0]
        if n == 0:
            return {"mean": 0.0, "variance": 0.0, "std_dev": 0.0}
            
        # Day 6: Statistical Moments from Raw Algebraic Equations
        raw_sum = 0.0
        # Fully vectorized mathematical sum to resolve in millisecond domain
        raw_sum = np.sum(vector)
        mean_val = raw_sum / n
        
        # Variance calculation from raw math: E[(X - mu)^2]
        deviation_squared = (vector - mean_val) ** 2
        variance_val = np.sum(deviation_squared) / n
        std_dev_val = np.sqrt(variance_val)
        
        return {
            "mean": float(mean_val),
            "variance": float(variance_val),
            "std_dev": float(std_dev_val)
        }
    except Exception as e:
        print(f"[FATAL] System mapping failure inside math engine: {str(e)}")
        raise

# Day 7: Performance Benchmark Verification Gate
if __name__ == "__main__":
    print("[INIT] Launching Day 1-7 Elite Standard Performance Verification...")
    
    start_time = time.time()
    
    # Step 1: Provision memory layout
    data_matrix = initialize_memory_matrix(rows=500000, cols=2)
    
    # Step 2: Clean data grid via vectorized masking
    cleaned_grid = process_vectorized_returns(data_matrix)
    
    # Step 3: Extract sample asset array for raw math
    target_vector = cleaned_grid[:, 0]
    
    # Step 4: Calculate algebraic statistics
    metrics = calculate_raw_moments(target_vector)
    
    execution_time_ms = (time.time() - start_time) * 1000
    
    print("\n" + "="*50)
    print("🏆 PERFORMANCE BENCHMARK RESULT (DAY 7 GATEWAY)")
    print(f"• Total Execution Time: {execution_time_ms:.2f} ms")
    print(f"• Processed Matrix Size: {data_matrix.shape[0]} Rows")
    print(f"• Raw Computed Mean: {metrics['mean']:.6f}")
    print(f"• Raw Computed Variance: {metrics['variance']:.6f}")
    print(f"• Raw Computed StdDev: {metrics['std_dev']:.6f}")
    print("="*50)
    
    # Assert benchmark resolves in millisecond domain (typically < 30ms)
    assert execution_time_ms < 100.0, "[BENCHMARK FAILED] Performance out of millisecond domain!"
    print("[SUCCESS] All Day 1-7 infrastructure constraints passed with Green Status.")
