import os
import polars as pl
import yfinance as yf
from datetime import datetime, timedelta

def download_and_partition_vault():
    base_dir = "quant_apprenticeship"
    raw_dir = os.path.join(base_dir, "data_feed")
    train_dir = os.path.join(base_dir, "in_sample_train")
    holdout_dir = os.path.join(base_dir, "absolute_holdout_vault")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(holdout_dir, exist_ok=True)

    tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS"]
    
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            continue
            
        data = data.reset_index()
        df = pl.from_pandas(data)
        
        clean_name = ticker.replace(".NS", "")
        raw_file_path = os.path.join(raw_dir, f"{clean_name}.parquet")
        df.write_parquet(raw_file_path, compression="snappy")

        total_rows = len(df)
        split_index = int(total_rows * 0.80)
        
        train_df = df.slice(0, split_index)
        holdout_df = df.slice(split_index, total_rows - split_index)
        
        train_save_path = os.path.join(train_dir, f"{clean_name}.parquet")
        holdout_save_path = os.path.join(holdout_dir, f"{clean_name}.parquet")
        
        train_df.write_parquet(train_save_path, compression="snappy")
        holdout_df.write_parquet(holdout_save_path, compression="snappy")

if __name__ == "__main__":
    download_and_partition_vault()
