import polars as pl
from datetime import time

def impute_missing_values(df: pl.DataFrame, asset_columns: list[str]) -> pl.DataFrame:
    """
    IIT-Bombay Balanced Quant Core - Day 18 Ingestion Shield.
    1. मार्केट ओपनिंग के समय (उदा. 09:15) अगर डेटा गायब है, तो उस पूरे दिन को ड्रॉप करता है।
    2. इंट्राडे के बाकी बचे गैप्स को बिना किसी Look-Ahead Bias के Forward-Fill करता है।
    """
    
    # स्टेप 1: सुनिश्चित करें कि आपका टाइमस्टैम्प कॉलम Datetime फॉर्मेट में हो
    df = df.with_columns(pl.col("timestamp").str.to_datetime())
    
    # स्टेप 2: मार्केट ओपनिंग (उदा. सुबह 09:15:00) के समय गायब डेटा वाले दिनों की पहचान करें
    # हम चेक कर रहे हैं कि क्या सुबह 09:15 पर कोई भी एसेट कॉलम Null है
    market_open_time = time(9, 15)
    
    bad_days = (
        df.filter(
            (pl.col("timestamp").dt.time() == market_open_time) & 
            (pl.any_horizontal(pl.col(asset_columns).is_null()))
        )
        .select(pl.col("timestamp").dt.date().alias("bad_date"))
        .distinct()
    )
    
    # स्टेप 3: अगर वो तारीखें 'bad_days' में हैं, तो उस पूरे दिन के ब्लॉक को ड्रॉप करें
    df = df.with_columns(pl.col("timestamp").dt.date().alias("temp_date"))
    df = df.join(bad_days, left_on="temp_date", right_on="bad_date", how="anti")
    df = df.drop("temp_date")
    
    # स्टेप 4: इंट्राडे के बाकी टाइम स्लॉट्स के लिए Zero-Bias Forward-Fill लागू करें
    # यह बिना किसी फ्यूचर डेटा को देखे (Look-ahead bias मुक्त) मिसिंग वैल्यूज को भरेगा
    df = df.with_columns([
        pl.col(col).fill_null(strategy="forward") for col in asset_columns
    ])
    
    return df

# --- टेस्ट रन (Simulated Example) ---
if __name__ == "__main__":
    # मान लेते हैं कि यह आपका कल का Outer-Joined Dataframe है
    raw_data = {
        "timestamp": [
            "2026-09-10 09:15:00", "2026-09-10 09:16:00", "2026-09-10 09:17:00",
            "2026-09-11 09:15:00", "2026-09-11 09:16:00", "2026-09-11 09:17:00"
        ],
        "Asset_A": [100.0, None, 100.5, None, 105.0, 105.2], # 11 तारीख को ओपनिंग मिसिंग है
        "Asset_B": [50.0, 50.1, None, 52.0, 52.1, 52.2]
    }
    
    df_joined = pl.DataFrame(raw_data)
    assets = ["Asset_A", "Asset_B"]
    
    print("--- प्रोसेसिंग से पहले (कल का आउटपुट) ---")
    print(df_joined)
    
    clean_df = impute_missing_values(df_joined, assets)
    
    print("\n--- आज का डे 18 प्रोसेस किया हुआ आउटपुट ---")
    print(clean_df)
