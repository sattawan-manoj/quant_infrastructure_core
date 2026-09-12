import os
import polars as pl
import time  # To check how fast our system is running

# ==========================================
# 🏠 STEP 1: Define your paths
# ==========================================
DATA_DIRECTORY = "./quant_apprenticeship/data_feed/cache/"
ASSET_NAME = "BTC_USD_5Year_Daily.parquet"  # Example asset file name
FULL_PATH = os.path.join(DATA_DIRECTORY, ASSET_NAME)

# Safety Shield: Create the cache directory if it does not exist
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
    print(f"📁 [SETUP] New folder created at: {DATA_DIRECTORY}")

# Start tracking time to benchmark execution speed
start_time = time.time()

# ==========================================
# 🛡️ STEP 2: DAY 20 LOCAL CACHE CHECK LAYER
# ==========================================
if os.path.exists(FULL_PATH):
    # --- ⚡ CACHE HIT MATRIX ---
    # If the file exists on your computer, do not touch the internet
    print("\n--------------------------------------------------")
    print(f"⚡ [CACHE HIT] File found! No internet/API needed.")
    print(f"📂 Loading directly from local drive: {FULL_PATH}")
    print("--------------------------------------------------")
    
    # Load the binary Parquet file directly from your hard drive
    df = pl.read_parquet(FULL_PATH)

else:
    # --- 🌐 CACHE MISS MATRIX ---
    # Triggered only if the file is completely missing from your computer
    print("\n--------------------------------------------------")
    print(f"🌐 [CACHE MISS] File not found! Preparing data...")
    print("--------------------------------------------------")
    
    # ----------------------------------------------------
    # 👉 [Your original DAY 19 logic runs here] 👈
    # ----------------------------------------------------
    print("⏳ Downloading data from API and locking Polars Schema...")
    
    # Creating a mock clean 5-year data frame for testing purposes
    # (When you add your real code, it will handle the download here)
    df = pl.DataFrame({
        "timestamp": pl.date_range(start=pl.date(2021, 1, 1), end=pl.date(2026, 1, 1), interval="1d", eager=True),
        "close": [100.0 + (i * 0.02) for i in range(1827)]
    })
    
    # --- 📦 DAY 19 BINARY SAVING LOGIC ---
    # Save the file immediately after downloading and cleaning for future use
    df.write_parquet(FULL_PATH, compression="snappy")
    print(f"📦 [DAY 19] Data successfully saved to Parquet with Snappy Compression.")

# ==========================================
# ⏱️ STEP 3: View the Performance Benchmark Live
# ==========================================
end_time = time.time()
execution_time = (end_time - start_time) * 1000 # Convert to milliseconds

print(f"\n📊 DataFrame Scale: {df.shape[0]} Rows")
print(f"⏱️ Total Execution Time: {execution_time:.2f} Milliseconds (ms)")
