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
    pl.col("daily_return").alias("signal_unsafe")
)

df = df.with_columns(
    pl.col("daily_return").shift(1).alias("signal_safe")
)

df_clean = df.drop_nulls()

cov_matrix_unsafe = np.cov(df_clean["signal_unsafe"], df_clean["daily_return"])
covariance_unsafe = cov_matrix_unsafe[0, 1]

cov_matrix_safe = np.cov(df_clean["signal_safe"], df_clean["daily_return"])
covariance_safe = cov_matrix_safe[0, 1]

print(f"Unsafe Covariance: {covariance_unsafe:.6f}")
print(f"Safe Covariance: {covariance_safe:.6f}")

try:
    assert np.isclose(covariance_safe, 0.0, atol=1e-5)
    print("SUCCESS: Look-Ahead Test Passed.")
except AssertionError:
    raise ValueError("ERROR: Data Leakage Detected.")
