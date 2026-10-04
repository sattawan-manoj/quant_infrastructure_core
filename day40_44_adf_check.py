import os
import numpy as np
import polars as pl
from statsmodels.tsa.stattools import adfuller

def compute_stable_rolling_ols(y_vector, x_vector, condition_limit=1000):
    X_design = np.vstack([x_vector, np.ones(len(x_vector))]).T
    condition_number = np.linalg.cond(X_design)
    
    if condition_number > condition_limit:
        return None
        
    beta_params = np.linalg.pinv(X_design.T @ X_design) @ X_design.T @ y_vector
    return beta_params 

def run_real_rolling_windows(y_data, x_data, window_size=60):
    total_points = len(y_data)
    all_residuals = [] 
    
    print(f"[PROCESS] Executing rolling window engine over {total_points} rows with window size: {window_size} days")

    for i in range(window_size, total_points):
        y_slice = y_data[i - window_size : i]
        x_slice = x_data[i - window_size : i]
        
        params = compute_stable_rolling_ols(y_slice, x_slice)
        
        if params is None:
            all_residuals.append(0.0) 
            continue
            
        hedge_ratio = params[0]
        intercept = params[1]
        
        current_y = y_data[i]
        current_x = x_data[i]
        
        residual_spread = current_y - (hedge_ratio * current_x + intercept)
        all_residuals.append(residual_spread)
        
    print(f"[SUCCESS] Rolling window iterations finalized. Total generated spread data points: {len(all_residuals)}")
    return np.array(all_residuals)

if __name__ == "__main__":
    possible_paths = [
        "/home/manoj/quant_apprenticeship/in_sample_train",
        "in_sample_train",
        "quant_apprenticeship/in_sample_train"
    ]
    
    train_dir = None
    for path in possible_paths:
        if os.path.exists(path):
            train_dir = path
            break
            
    if train_dir is not None:
        asset_x_path = os.path.join(train_dir, "RELIANCE.parquet")
        asset_y_path = os.path.join(train_dir, "TCS.parquet")
        
        if os.path.exists(asset_x_path) and os.path.exists(asset_y_path):
            df_x = pl.read_parquet(asset_x_path)
            df_y = pl.read_parquet(asset_y_path)
            
            df_x = df_x.rename({col: "Date" if "Date" in col else "Close" if "Close" in col else col for col in df_x.columns})
            df_y = df_y.rename({col: "Date" if "Date" in col else "Close" if "Close" in col else col for col in df_y.columns})
            
            df_x = df_x.select(["Date", "Close"]).rename({"Close": "price_x"})
            df_y = df_y.select(["Date", "Close"]).rename({"Close": "price_y"})
            
            combined_df = df_x.join(df_y, on="Date", how="inner").sort("Date")
            combined_df = combined_df.drop_nulls()
            
            combined_df = combined_df.with_columns([
                pl.col("price_x").log().alias("log_x"),
                pl.col("price_y").log().alias("log_y")
            ])
            
            combined_df = combined_df.drop_nulls()
            
            real_x = combined_df["log_x"].to_numpy().flatten()
            real_y = combined_df["log_y"].to_numpy().flatten()
            
            historical_spreads = run_real_rolling_windows(real_y, real_x, window_size=60)
            
            print("\n[TELEMETRY] Head array execution print logs:")
            print(historical_spreads[:5])
            
            print("\n[PROCESS] Launching Augmented Dickey-Fuller Unit Root structural check...")
            
            try:
                clean_spreads = historical_spreads[historical_spreads != 0.0]
                
                adf_result = adfuller(clean_spreads, autolag='AIC')
                adf_statistic = adf_result[0]
                p_value = adf_result[1]
                critical_values = adf_result[4]
                
                print("\n=== ADF STATISTICAL REPORT ===")
                print(f"ADF Test Statistic: {adf_statistic:.4f}")
                print(f"P-Value: {p_value:.6f}")
                print("Critical Values Breakdown:")
                for key, val in critical_values.items():
                    print(f"   {key}: {val:.4f}")
                
                if p_value < 0.05:
                    print("\n[STATUS] GREEN: Spread vector displays stationary, mean-reverting behavior.")
                else:
                    print("\n[STATUS] RED: Spread vector failed stationarity parameters. Put tracking pair to sleep.")
                    
            except Exception as adf_error:
                print(f"\n[FATAL MATH FAILURE] ADF computation broke down due to vector issues: {adf_error}")
