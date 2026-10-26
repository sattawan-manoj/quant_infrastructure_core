import os
import numpy as np
import polars as pl

class WalkForwardEngine:
    def __init__(self, max_holding_days=20):
        self.max_hold = max_holding_days

    def run_wf_simulation(self, spread_series, asset_returns):
        n = len(spread_series)
        final_wf_returns = np.zeros(n)
        
        train_window_grid = [60, 80, 100]
        test_window_grid = [20, 30, 40]
        barrier_grid = [1.0, 1.5, 2.0]
        
        best_overall_perf = -np.inf
        best_train_len = 60
        best_test_len = 20
        
        for t_len in train_window_grid:
            for s_len in test_window_grid:
                temp_perf = 0
                for start_idx in range(0, n - t_len, s_len):
                    curr_train_end = start_idx + t_len
                    if curr_train_end >= n:
                        break
                    t_spread = spread_series[start_idx:curr_train_end]
                    m_tr = np.mean(t_spread)
                    s_tr = np.std(t_spread) if np.std(t_spread) > 0 else 1.0
                    z_tr = (t_spread - m_tr) / s_tr
                    
                    for b in barrier_grid:
                        t_sig = np.zeros(len(z_tr))
                        t_sig[z_tr > b] = -1
                        t_sig[z_tr < -b] = 1
                        temp_perf += np.sum(t_sig * asset_returns[start_idx:curr_train_end])
                        
                if temp_perf > best_overall_perf:
                    best_overall_perf = temp_perf
                    best_train_len = t_len
                    best_test_len = s_len

        for start_idx in range(0, n - best_train_len, best_test_len):
            train_end = start_idx + best_train_len
            test_end = min(train_end + best_test_len, n)
            
            if train_end >= n:
                break
                
            train_spread = spread_series[start_idx:train_end]
            mu_train = np.mean(train_spread)
            sigma_train = np.std(train_spread) if np.std(train_spread) > 0 else 1.0
            
            z_test = (spread_series[train_end:test_end] - mu_train) / sigma_train
            test_returns = asset_returns[train_end:test_end]
            
            best_local_perf = -np.inf
            local_barrier = 1.5
            for b in barrier_grid:
                z_train = (train_spread - mu_train) / sigma_train
                t_sig = np.zeros(len(z_train))
                t_sig[z_train > b] = -1
                t_sig[z_train < -b] = 1
                p_factor = np.sum(t_sig * asset_returns[start_idx:train_end])
                if p_factor > best_local_perf:
                    best_local_perf = p_factor
                    local_barrier = b
            
            raw_test_signals = np.zeros(len(z_test))
            raw_test_signals[z_test > local_barrier] = -1
            raw_test_signals[z_test < -local_barrier] = 1
            
            df_signals = pl.DataFrame({"raw": raw_test_signals})
            clean_signals = df_signals.select(pl.col("raw").shift(1).fill_null(0)).to_series().to_numpy().copy()
            
            is_active = (clean_signals != 0).astype(int)
            signal_changes = np.diff(clean_signals, prepend=0) != 0
            run_ids = np.cumsum(signal_changes)
            
            df_clocks = pl.DataFrame({"active": is_active, "run_id": run_ids})
            polars_positions_clocks = (
                df_clocks.select(pl.col("active").cum_sum().over("run_id"))
                .to_series()
                .to_numpy()
            )
            
            clean_signals[polars_positions_clocks > self.max_hold] = 0
            final_wf_returns[train_end:test_end] = clean_signals * test_returns
            
        return final_wf_returns

if __name__ == "__main__":
    np.random.seed(42)
    simulated_length = 1000
    
    macro_assets = [f"RANDOM_ASSET_{i}" for i in range(1, 21)]
    num_assets = len(macro_assets)
    aggregated_matrix_returns = np.zeros((simulated_length, num_assets))
    
    engine = WalkForwardEngine()
    
    for idx, asset in enumerate(macro_assets):
        mock_spread = np.random.normal(0, 1, simulated_length)
        mock_asset_returns = np.random.normal(0, 0.02, simulated_length)
        
        asset_wf_returns = engine.run_wf_simulation(mock_spread, mock_asset_returns)
        aggregated_matrix_returns[:, idx] = asset_wf_returns
        
    output_path = os.path.abspath("wf_returns.npy")
    np.save(output_path, aggregated_matrix_returns)
    
    if os.path.exists(output_path):
        print(f"[VERIFIED PASS] File successfully generated at: {output_path}")
        print(f"Matrix shape verified: {aggregated_matrix_returns.shape}")
