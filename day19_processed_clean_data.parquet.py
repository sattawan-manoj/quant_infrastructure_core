import polars as pl
from datetime import time
import os

def impute_missing_values(df: pl.DataFrame, asset_columns: list[str]) -> pl.DataFrame:
    """
    1. Drops the entire day if data is missing at market opening time (e.g., 09:15).
    2. Applies a Zero-Bias Forward-Fill for any remaining intraday gaps to eliminate Look-Ahead Bias.
    """
    # Step 1: Ensure the timestamp column is in Datetime format
    df = df.with_columns(pl.col("timestamp").str.to_datetime())
    
    # Step 2: Identify bad days where data is missing at market opening time
    market_open_time = time(9, 15)
    
    bad_days = (
        df.filter(
            (pl.col("timestamp").dt.time() == market_open_time) & 
            (pl.any_horizontal(pl.col(asset_columns).is_null()))
        )
        .select(pl.col("timestamp").dt.date().alias("bad_date"))
        .distinct()
    )
    
    # Step 3: Drop the entire day if its date is present in the bad_days list (Anti-Join)
    df = df.with_columns(pl.col("timestamp").dt.date().alias("temp_date"))
    df = df.join(bad_days, left_on="temp_date", right_on="bad_date", how="anti")
    df = df.drop("temp_date")
    
    # Step 4: Apply Zero-Bias Forward-Fill for the remaining intraday slots
    df = df.with_columns([
        pl.col(col).fill_null(strategy="forward") for col in asset_columns
    ])
    
    return df

def save_as_parquet(df: pl.DataFrame, file_name: str):
    """
    Serializes and saves the cleaned DataFrame into a binary compressed Parquet format.
    """
    print("\n--- Starting Parquet Serialization ---")
    
    # .write_parquet stores data column-wise instead of row-wise
    # compression="snappy" shrinks the file size down significantly up to 80%
    df.write_parquet(file_name, compression="snappy")
    
    print(f"🎉 Success! Your compressed file has been saved at: {os.path.abspath(file_name)}")

# --- Test Run (Combined execution of Day 18 + Day 19) ---
if __name__ == "__main__":
    # Simulated raw data matrix
    raw_data = {
        "timestamp": [
            "2026-09-10 09:15:00", "2026-09-10 09:16:00", "2026-09-10 09:17:00",
            "2026-09-11 09:15:00", "2026-09-11 09:16:00", "2026-09-11 09:17:00"
        ],
        "Asset_A": [100.0, None, 100.5, None, 105.0, 105.2], # Missing opening data on 11th
        "Asset_B": [50.0, 50.1, None, 52.0, 52.1, 52.2]
    }
    
    df_joined = pl.DataFrame(raw_data)
    assets = ["Asset_A", "Asset_B"]
    
    print("--- Before Processing (Yesterday's Joined Output) ---")
    print(df_joined)
    
    # 1. Processing and cleaning the data gaps (Day 18 logic)
    clean_df = impute_missing_values(df_joined, assets)
    
    print("\n--- Today's Day 18 Processed Clean Output ---")
    print(clean_df)
    
    # 2. Saving the clean data into binary Parquet format (Day 19 logic)
    output_filename = "processed_clean_data.parquet"
    save_as_parquet(clean_df, output_filename)
