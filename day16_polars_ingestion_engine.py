import polars as pl
import os
import time

def build_strict_ingestion_pipeline(file_path: str) -> pl.DataFrame:
    """
    IIT-Bombay Balanced Quant Core: Day 16 Ingestion Pipeline.
    """
    strict_schema = {
        "timestamp": pl.Datetime(time_unit="us"),
        "symbol": pl.Categorical,
        "open": pl.Float64,
        "high": pl.Float64,
        "low": pl.Float64,
        "close": pl.Float64,
        "volume": pl.Int64
    }
    
    print(f"[INGESTION] Creating LazyFrame connection to: {file_path}")
    
    lazy_pipeline = (
        pl.scan_csv(
            file_path,
            schema=strict_schema,  
            has_header=True,
            try_parse_dates=True   
        )
        .select([
            "timestamp", "symbol", "open", "high", "low", "close", "volume"
        ])
    )
    
    print("[INGESTION] Query plan optimized. Executing materialization via .collect()...")
    final_dataframe = lazy_pipeline.collect()
    return final_dataframe

# === ड्राइवर टेस्ट ब्लॉक ===
if __name__ == "__main__":
    dummy_file = "test_tick_data.csv"
    
    with open(dummy_file, "w") as f:
        f.write("timestamp,symbol,open,high,low,close,volume\n")
        f.write("2026-09-08 09:15:00,RELIANCE,2500.0,2510.0,2495.0,2505.0,150000\n")
        f.write("2026-09-08 09:16:00,RELIANCE,2505.0,2515.0,2502.0,2512.0,180000\n")
        
    try:
        df = build_strict_ingestion_pipeline(dummy_file)
        
        print("\n🟢 [SUCCESS] Data successfully ingested with zero formatting errors!")
        print("--- DataFrame Schema Details ---")
        print(df.schema)
        print("\n--- First 2 Rows of Data ---")
        print(df.head(2))
        
    except Exception as e:
        print(f"🔴 [ERROR] Pipeline failed: {e}")
        
    finally:
        print("\n⏳ फ़ाइल बन चुकी है, अगले 5 सेकंड तक बाएँ (left) साइड के फोल्डर पैनल में चेक करो...")
        time.sleep(5) 
        
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
            print("🗑️ 5 सेकंड पूरे! 'finally' ने टेस्ट फ़ाइल को डिस्क से डिलीट कर दिया है।")
