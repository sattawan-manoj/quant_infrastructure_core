import numpy as np
import polars as pl

asset_list = [
    "NIFTY_50", "BANK_NIFTY", "RELIANCE", "TCS", "INFY", 
    "HDFCBANK", "ICICIBANK", "GOLD_USD", "SILVER_USD", "CRUDE_OIL",
    "USD_INR", "EUR_INR", "GBP_USD", "APPLE", "MICROSOFT",
    "TESLA", "AMAZON", "GOOGLE", "BITCOIN_USD", "US_10Y_BOND"
]

for asset_name in asset_list:
    num_rows = 50000
    random_returns = np.random.normal(0.0001, 0.01, num_rows)
    price_series = 100.0 * np.exp(np.cumsum(random_returns))
    
    df = pl.DataFrame({
        "daily_return": random_returns,
        "stock_price": price_series
    })
    
    df = df.with_columns(
        pl.col("daily_return").shift(1).alias("signal_safe")
    )
    
    df_clean = df.drop_nulls()
    
    cov_matrix_safe = np.cov(df_clean["signal_safe"], df_clean["daily_return"])
    covariance_safe = cov_matrix_safe[0, 1]
    
    try:
        assert np.isclose(covariance_safe, 0.0, atol=1e-5)
        print(f"{asset_name}: PASSED")
    except AssertionError:
        raise ValueError(f"ERROR: Data Leakage at {asset_name}")
