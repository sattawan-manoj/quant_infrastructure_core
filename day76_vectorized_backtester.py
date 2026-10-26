import numpy as np
import polars as pl
import pandas as pd

class VectorizedBacktester:
    def __init__(self, df: pl.DataFrame, train_size: int = 252, test_size: int = 63):
        self.df = df.sort("timestamp")
        self.total_rows = self.df.height
        
        self.train_size = train_size  
        self.test_size = test_size    
        
        self.assets = [col for col in self.df.columns if col != "timestamp"]
        
        print(f"[INIT] Total data rows: {self.total_rows}")
        print(f"[CONFIG] Train Window: {self.train_size} days | Test Window: {self.test_size} days\n")

    def run_walk_forward(self):
        start_idx = 0
        step = 1

        while (start_idx + self.train_size + self.test_size) <= self.total_rows:
            
            train_end_idx = start_idx + self.train_size
            train_shard = self.df.slice(start_idx, self.train_size)
            
            test_end_idx = train_end_idx + self.test_size
            test_shard = self.df.slice(train_end_idx, self.test_size)
            
            print(f"--- [STEP {step}] ---")
            print(f"Train Indices: {start_idx:4d} to {train_end_idx:4d} | Rows: {train_shard.height}")
            print(f"Test Indices : {train_end_idx:4d} to {test_end_idx:4d} | Rows: {test_shard.height}")
            
            
            start_idx += self.test_size
            step += 1

        last_idx = start_idx + self.train_size
        residual_rows = self.total_rows - last_idx
        
        print("\n==========================================================================")
        print(f"✅ [SUCCESS] Walk-forward loop finished. Total steps: {step - 1}")
        print(f"[TAIL REPORT] Loop halted at row index: {last_idx}")
        print(f"[ANALYSIS] Total residual rows dropped: {residual_rows}")
        
        if residual_rows > 0:
            print(f"⚠️  Safety Guardrail Notification: Indices from {last_idx} to {self.total_rows} were dropped.")
            print("   Reason: Remaining sample size is insufficient to build a complete test block.")
        print("==========================================================================")


if __name__ == "__main__":
    print("[TEST RUN] Initializing dataset structure (1310 Rows)...")
    
    np.random.seed(42)
    date_range = pd.date_range(start="2020-01-01", periods=1310, freq="D")
    mock_data = {"timestamp": date_range}
    for i in range(1, 21):
        mock_data[f"ASSET_{i:02d}"] = np.random.normal(100, 5, 1310)
    
    production_df = pl.DataFrame(mock_data)
    
    backtester = VectorizedBacktester(df=production_df)
    backtester.run_walk_forward()
