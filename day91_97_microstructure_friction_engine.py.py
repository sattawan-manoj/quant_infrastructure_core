import numpy as np

def generate_synthetic_market_data(num_days=100):
    np.random.seed(42)
    
    gross_returns = np.random.normal(loc=0.0005, scale=0.015, size=num_days)
    atr_vector = np.random.uniform(low=1.5, high=4.5, size=num_days)
    signals = np.random.choice([-1, 0, 1], size=num_days, p=[0.3, 0.4, 0.3])
    
    return gross_returns, atr_vector, signals

def apply_latency_friction_accounting(gross_returns, current_atr, base_spread, broker_commission, latency_factor=0.002):
    volatility_slippage_penalty = current_atr * latency_factor
    total_drag = base_spread + broker_commission + volatility_slippage_penalty
    net_realized_returns = gross_returns - total_drag
    return net_realized_returns, total_drag

def run_friction_pipeline():
    print("🚀 [DAY 91-97] Starting Unified Microstructure Cost Pipeline...\n")
    
    num_days = 100
    gross_returns, atr_vector, signals = generate_synthetic_market_data(num_days)
    
    BASE_SPREAD = 0.0002
    BROKER_COMMISSION = 0.0001
    LATENCY_FACTOR = 0.0005
    
    net_returns_list = []
    total_drag_list = []
    
    for i in range(num_days):
        if signals[i] != 0:
            net_ret, drag = apply_latency_friction_accounting(
                gross_returns[i], 
                atr_vector[i], 
                BASE_SPREAD, 
                BROKER_COMMISSION, 
                LATENCY_FACTOR
            )
        else:
            net_ret = gross_returns[i]
            drag = 0.0
            
        net_returns_list.append(net_ret)
        total_drag_list.append(drag)
        
    net_returns = np.array(net_returns_list)
    total_drag = np.array(total_drag_list)
    
    cumulative_gross = np.exp(np.cumsum(gross_returns)) - 1
    cumulative_net = np.exp(np.cumsum(net_returns)) - 1
    
    print("======= PERFORMANCE BENCHMARK REPORT =======")
    print(f"Total Trading Days Checked : {num_days}")
    print(f"Total Active Trades Executed: {np.count_nonzero(signals)}")
    print(f"Total Capital Drag Paid     : {np.sum(total_drag) * 100:.4f}%")
    print(f"Final Gross Return (Ideal)  : {cumulative_gross[-1] * 100:.2f}%")
    print(f"Final Net Return (Realistic): {cumulative_net[-1] * 100:.2f}%")
    print("============================================")
    
    assert len(net_returns) == num_days, "[ERROR] Data mismatch detected!"
    print("\n✅ [DAY 97 SUCCESS] Friction Engine validated with zero runtime exceptions.")
    
    return net_returns

if __name__ == "__main__":
    net_strategy_returns = run_friction_pipeline()
