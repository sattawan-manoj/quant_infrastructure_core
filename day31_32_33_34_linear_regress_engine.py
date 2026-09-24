import numpy as np

def compute_stable_rolling_ols(y_vector, x_vector, condition_limit=1000):
    X_design = np.vstack([x_vector, np.ones(len(x_vector))]).T
    condition_number = np.linalg.cond(X_design)
    
    if condition_number > condition_limit:
        print(f"[REGRESSION WARNING] Matrix ill-conditioned: {condition_number:.2f}. Dropping current window.")
        return None, None
    
    X_transpose_X = X_design.T @ X_design
    beta_params = np.linalg.pinv(X_transpose_X) @ X_design.T @ y_vector
    
    hedge_ratio = beta_params[0]
    intercept = beta_params[1]
    
    return hedge_ratio, intercept

if __name__ == "__main__":
    print("🔄 Testing Day 34 Linear Matrix Stability Core...")
    
    np.random.seed(42)
    asset_X = np.random.randn(100)
    asset_Y = 1.2 * asset_X + np.random.randn(100) * 0.1
    
    hr, intercept = compute_stable_rolling_ols(asset_Y, asset_X)
    print(f"✅ Normal Matrix Pass -> Hedge Ratio: {hr:.4f}, Intercept: {intercept:.4f}\n")
    
    bad_X = np.linspace(1, 10, 100)
    bad_Y = bad_X * 1.000000001
    
    print("🔄 Testing Unstable Matrix (Should trigger warning and return None)...")
    hr_bad, int_bad = compute_stable_rolling_ols(bad_Y, bad_X, condition_limit=10)
    print(f"Result: Hedge Ratio = {hr_bad}, Intercept = {int_bad}")
