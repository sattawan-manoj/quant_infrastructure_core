import polars as pl
import numpy as np
from datetime import datetime, timedelta

print("="*60)
print("🚀 STARTING DAY 23: ISOLATED LOG RETURNS ENGINE")
print("="*60)

# STEP 1: Generate 5 years of synthetic asset price history
print("\n[STEP 1] Generating 5 years of isolated asset data...")
start_date = datetime(2021, 1, 1)
total_days = 5 * 365 

np.random.seed(42)  
dates_list = [start_date + timedelta(days=i) for i in range(total_days)]
price_changes = np.random.normal(0.0005, 0.01, total_days)  
prices_list = 100.0 * np.exp(np.cumsum(price_changes))  

df = pl.DataFrame({
    "timestamp": dates_list,
    "close_price": prices_list
})
print(f"📊 Matrix Created Natively: {df.shape} rows of data locked.")

# STEP 2: Vectorized continuous log returns math execution: \ln(P_t / P_{t-1})
print("\n[STEP 2] Running high-speed vectorization math without loops...")
df = df.with_columns([
    (pl.col("close_price") / pl.col("close_price").shift(1)).log().alias("log_returns")
])

# STEP 3: Console matrix verification output
print("\n[STEP 3] Reviewing structural matrix sample:")
print(df.head(7))  

# STEP 4: Serialize clean matrix to an isolated binary Parquet container
output_path = "day23_isolated_log_returns.parquet"
df.write_parquet(output_path, compression="snappy")

print("\n" + "="*60)
print(f"✅ SUCCESS: Isolated Day 23 matrix saved directly to disk!")
print(f"📁 File Destination: {output_path}")
print("="*60)
