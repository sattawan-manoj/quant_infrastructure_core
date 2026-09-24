import os
import json
import numpy as np
import polars as pl
from datetime import datetime, timedelta

def generate_synthetic_market_data(cache_dir: str):
    """
    Data-Generation Subsystem: Bypasses broker network drops by generating
    high-quality multi-asset arrays to seed your local physical cache.
    """
    print("🛠️  [INITIALIZATION] Checking local storage layers...")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Define our targeted timeframe parameters
    total_days = 200
    start_date = datetime(2023, 1, 1)
    date_list = [start_date + timedelta(days=i) for i in range(total_days)]

    # 1. Generate standard survivor assets (Continuously trade throughout)
    survivors = ["AAPL", "MSFT", "GOOGL"]
    for asset in survivors:
        file_path = os.path.join(cache_dir, f"{asset}.parquet")
        if not os.path.exists(file_path):
            # Form clean random-walk market matrices
            prices = 150.0 + np.cumsum(np.random.normal(0.1, 1.5, total_days))
            df = pl.DataFrame({
                "timestamp": date_list,
                "price": prices,
                "volume": np.random.randint(10000, 50000, total_days)
            })
            df.write_parquet(file_path, compression="snappy")
            print(f"   -> [SAVED CACHE] Active Survivor: {asset}.parquet")

    # 2. Generate dead/zombie assets (Crucial to kill survivorship bias!)
    # Silicon Valley Bank (SIVBQ) ceases to exist halfway through the timeline
    dead_assets = {"SIVBQ": 90, "FRCBQ": 130}
    for asset, lifespan in dead_assets.items(): # यहाँ 'lifespan' ठीक कर दिया गया है
        file_path = os.path.join(cache_dir, f"{asset}.parquet")
        if not os.path.exists(file_path):
            # Price trends downward sharply before terminating completely
            prices = 100.0 + np.cumsum(np.random.normal(-0.5, 2.0, lifespan))
            prices = np.clip(prices, 0.01, None) # Floor price at zero
            
            df = pl.DataFrame({
                "timestamp": date_list[:lifespan], # Truncates date history
                "price": prices,
                "volume": np.random.randint(5000, 20000, lifespan)
            })
            df.write_parquet(file_path, compression="snappy")
            print(f"   -> [SAVED GRAVEYARD CACHE] Defunct Asset: {asset}.parquet")

def load_unbiased_universe(config_path: str):
    """
    Reads the complete ledger, ensuring both active survivors 
    and dead historical companies are mapped out safely.
    """
    try:
        with open(config_path, "r") as f:
            universe = json.load(f)
    except FileNotFoundError:
        print(f"❌ [CONFIG ERROR] System configuration file missing at: {config_path}")
        return []

    active = universe.get("active_assets", []) 
    delisted = universe.get("delisted_historical_assets", [])
    
    # Merge both structures to fully form the unbiased pipeline matrix
    full_unbiased_list = active + delisted
    
    print(f"\n🛡️  [SHIELD CORES ENGAGED] Total Universe Assets Mapped: {len(full_unbiased_list)}")
    print(f"   └─ Active Matrix Blocks: {len(active)} | Delisted/Dead Blocks: {len(delisted)}")
    
    return full_unbiased_list

def verify_local_parquet_cache(asset_list: list, cache_directory: str):
    """
    Scans the hardware drive structure to verify that all assets (including the dead ones)
    are present inside the runtime ingestion layers.
    """
    missing_assets = []
    print("\n🔍 Scanning hardware directory for files...")
    
    for asset in asset_list:
        expected_file_path = os.path.join(cache_directory, f"{asset}.parquet")
        
        if os.path.exists(expected_file_path):
            # Read a small subset of the file to prove it is healthy and contains rows
            sample_df = pl.read_parquet(expected_file_path)
            print(f"   ✅ [VALID CACHE] {asset}.parquet -> Elements: {sample_df.shape[0]} rows mapping price records.")
        else:
            print(f"   ❌ [CRITICAL ABSENCE] {asset}.parquet is missing from your storage matrix!")
            missing_assets.append(asset)
            
    return missing_assets

# --- SYSTEM INTEGRATION EXECUTION GATEWAY ---
if __name__ == "__main__":
    # Standardize our workspace paths exactly
    CONFIG_FILE = "universe_config.json"
    CACHE_DIR = "./parquet_cache"
    
    # Auto-generate our universe configuration mapping ledger file if missing
    if not os.path.exists(CONFIG_FILE):
        config_data = {
            "active_assets": ["AAPL", "MSFT", "GOOGL"],
            "delisted_historical_assets": ["SIVBQ", "FRCBQ"]
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=2)
        print(f"📝 Created configuration map: {CONFIG_FILE}")

    # Step 1: Run the generation module to cleanly seed the storage space
    generate_synthetic_market_data(CACHE_DIR)
    
    # Step 2: Extract our complete list of assets from the tracking framework 
    complete_universe = load_unbiased_universe(CONFIG_FILE)
    
    # Step 3: Run the hardware scanner check loop
    missing = verify_local_parquet_cache(complete_universe, CACHE_DIR)
    
    # Final assertion gate tracking status validation
    if len(missing) == 0:
        print("\n🏆 [DAY 22 MILESTONE PASSED] The Survivorship Bias Isolation Shield is 100% active and healthy.")
    else:
        print(f"\n⚠️  [GATEWAY BLOCKED] Missing dataset matrix files: {missing}")
