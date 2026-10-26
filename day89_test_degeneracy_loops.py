import numpy as np

def execute_day89_degeneracy_check():
    returns_matrix = np.load("wf_returns.npy")
    
    num_assets = returns_matrix.shape[1]
    gross_positive_returns = np.zeros(num_assets)
    
    for i in range(num_assets):
        asset_vector = returns_matrix[:, i]
        gross_positive_returns[i] = np.sum(asset_vector[asset_vector > 0])
        
    total_gross_systematic_returns = np.sum(gross_positive_returns)
    
    max_asset_contribution = np.max(gross_positive_returns)
    concentration_ratio = max_asset_contribution / total_gross_systematic_returns
    
    print(f"[DEGENERACY AUDIT] Concentration Ratio: {concentration_ratio:.2%}")
    
    assert concentration_ratio <= 0.70, \
        f"[FATAL DEGENERACY EXCEPTION] Strategy Overfitted! {concentration_ratio:.2%} of gross systematic returns are concentrated inside a singular asset window."
        
    print("[SUCCESS] Day 89 Audit Cleared. Returns are structurally distributed.")
    return True

if __name__ == "__main__":
    execute_day89_degeneracy_check()
