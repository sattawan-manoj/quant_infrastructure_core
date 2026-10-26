import os
import json
import numpy as np

def run_live_ols_and_fdr_checks(asset_returns):
    n = len(asset_returns)
    x_trend = np.arange(n)
    X_design = np.vstack([x_trend, np.ones(n)]).T
    
    condition_number = np.linalg.cond(X_design)
    if condition_number > 1000:
        return False, 1.0, 0.0
        
    beta_params = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ asset_returns
    residuals = asset_returns - (X_design @ beta_params)
    
    residual_variance = np.var(residuals) if np.var(residuals) > 0 else 1.0
    mock_t_stat = np.mean(asset_returns) / (np.sqrt(residual_variance / n) + 1e-9)
    p_value = float(2 * (1 - 1.0 / (1.0 + np.exp(-abs(mock_t_stat))))) 
    
    return True, p_value, float(beta_params)

def execute_strict_day90_gateway():
    print("\n🏛️ [IIT-BOMBAY QUANT] DAY 90: ENFORCING OLS & FDR LIVE GATEWAY")
    print("================================================================================")
    
    matrix_file = "wf_returns.npy"
    if not os.path.exists(matrix_file):
        raise FileNotFoundError(f"[CRITICAL] '{matrix_file}' matrix missing! Run core code first.")
        
    returns_matrix = np.load(matrix_file)
    simulated_length, num_assets = returns_matrix.shape
    print(f"[DATA] Ingested Random Matrix: {simulated_length} rows x {num_assets} assets.")
    
    gross_positive_returns = np.sum(np.maximum(returns_matrix, 0), axis=0)
    total_gross = np.sum(gross_positive_returns)
    concentration_ratio = np.max(gross_positive_returns) / (total_gross + 1e-9) if total_gross > 0 else 0.0
    
    assert concentration_ratio <= 0.70, "[FATAL DEGENERACY] Strategy Overfitted!"
    print(f"Camp: Day 89 Audit Cleared. Concentration Index: {concentration_ratio:.2%}")

    asset_ledger_matrix = {}
    macro_assets = [f"RANDOM_ASSET_{i}" for i in range(1, num_assets + 1)]
    
    p_values_list = []
    ols_results = {}
    
    for i in range(num_assets):
        asset_name = macro_assets[i]
        asset_returns = returns_matrix[:, i]
        
        is_stable, p_val, hedge_ratio = run_live_ols_and_fdr_checks(asset_returns)
        p_values_list.append(p_val)
        ols_results[asset_name] = {"is_stable": is_stable, "hedge_ratio": hedge_ratio}

    sorted_indices = np.argsort(p_values_list)
    m_space = len(p_values_list)
    alpha_target = 0.05
    fdr_reject_flags = np.zeros(m_space, dtype=bool)
    
    for rank, idx in enumerate(sorted_indices):
        critical_value = ((rank + 1) / m_space) * alpha_target
        if p_values_list[idx] <= critical_value:
            fdr_reject_flags[idx] = True

    for i in range(num_assets):
        asset_name = macro_assets[i]
        asset_returns = returns_matrix[:, i]
        
        equity_curve = np.exp(np.cumsum(asset_returns))
        running_max = np.maximum.accumulate(equity_curve)
        drawdowns = (equity_curve - running_max) / (running_max + 1e-9)
        max_drawdown = np.min(drawdowns)
        
        winning = asset_returns[asset_returns > 0]
        losing = asset_returns[asset_returns < 0]
        win_prob = len(winning) / len(asset_returns) if len(asset_returns) > 0 else 0
        ratio = np.mean(winning) / (abs(np.mean(losing)) + 1e-9) if len(losing) > 0 else 1
        clamped_kelly = np.clip(win_prob - ((1 - win_prob) / ratio), 0.0, 0.25)
            
        sorted_returns = np.sort(asset_returns)
        cutoff_index = np.maximum(1, int(0.05 * len(sorted_returns)))
        cvar_boundary = -np.mean(sorted_returns[:cutoff_index])
        
        asset_ledger_matrix[asset_name] = {
            "ols_estimation_parameters": {
                "inversion_stability_pass": ols_results[asset_name]["is_stable"],
                "dynamic_calculated_hedge_ratio": round(ols_results[asset_name]["hedge_ratio"], 6)
            },
            "false_discovery_rate_fdr_shield": {
                "raw_calculated_p_value": round(p_values_list[i], 6),
                "benjamini_hochberg_reject_null": bool(fdr_reject_flags[i])
            },
            "risk_and_allocation_shields": {
                "fractional_kelly_weight": round(float(clamped_kelly), 4),
                "95_pct_cvar_expected_shortfall": round(float(cvar_boundary), 6),
                "max_historical_drawdown_pct": round(float(max_drawdown * 100), 2),
                "final_wealth_peak": round(float(equity_curve[-1]), 4)
            }
        }
        print(f"-> Integrated Matrix Configuration for {asset_name}")

    master_payload = {
        "global_portfolio_meta": {
            "system_concentration_ratio": round(float(concentration_ratio), 4),
            "total_assets_validated": num_assets,
            "status": "COMPUTATIONAL_CORE_LOCKED"
        },
        "optimized_parameters_ledger_matrix": asset_ledger_matrix
    }
    
    output_ledger_path = os.path.abspath("backtest_performance_ledger.json")
    with open(output_ledger_path, "w") as storage_file:
        json.dump(master_payload, storage_file, indent=4)
        
    print("================================================================================")
    print(f"🚀 [DAY 90 GATEWAY CONQUEST SUCCESS] Ledger successfully locked at:\n   {output_ledger_path}\n")

if __name__ == "__main__":
    execute_strict_day90_gateway()
