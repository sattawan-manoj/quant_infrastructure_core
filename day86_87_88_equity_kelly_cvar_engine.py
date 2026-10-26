import numpy as np

def generate_risk_metrics_matrix(returns_path="wf_returns.npy"):
    returns = np.load(returns_path)
    
    equity_curve = np.exp(np.cumsum(returns))
    
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (equity_curve - running_max) / running_max
    max_drawdown = np.min(drawdowns)
    
    confidence_level = 0.05
    sorted_returns = np.sort(returns)
    
    cutoff_index = np.maximum(1, int(confidence_level * len(sorted_returns)))
    
    cvar_boundary = -np.mean(sorted_returns[:cutoff_index])
    
    return equity_curve, max_drawdown, cvar_boundary

if __name__ == "__main__":
    eq, max_dd, cvar = generate_risk_metrics_matrix()
    
    print(f"Equity Peak: {eq[-1]:.4f} | Max Drawdown: {max_dd*100:.2f}% | 95% CVaR Bound (Expected Shortfall): {cvar*100:.4f}%")
