import os
import numpy as np
import polars as pl

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
                pl.col("price_x").log().diff().alias("return_x"),
                pl.col("price_y").log().diff().alias("return_y")
            ])
            
            combined_df = combined_df.drop_nulls()
            
            real_x = combined_df["return_x"].to_numpy().flatten()
            real_y = combined_df["return_y"].to_numpy().flatten()
            
            historical_spreads = run_real_rolling_windows(real_y, real_x, window_size=60)
            
            print("\n[TELEMETRY] Head array execution print logs:")
            print(historical_spreads[:5])
