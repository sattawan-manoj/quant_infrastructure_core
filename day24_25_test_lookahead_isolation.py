import numpy as np
import polars as pl

np.random.seed(42)
num_rows = 50000
random_returns = np.random.normal(0.0001, 0.01, num_rows)
price_series = 100.0 * np.exp(np.cumsum(random_returns))

df = pl.DataFrame({
    "daily_return": random_returns,
    "stock_price": price_series
})

df = df.with_columns(
    pl.col("daily_return").alias("indicator_raw")
)

df_shielded = df.with_columns(
    pl.col("indicator_raw").shift(1).alias("trading_decision_safe")
)

print(df_shielded.head(5))
