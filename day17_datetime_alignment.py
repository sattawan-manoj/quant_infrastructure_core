import polars as pl
from datetime import datetime

def align_asset_datetimes(asset_a_path: str, asset_b_path: str) -> pl.DataFrame:
    """
    IIT-Bombay Quant Masterplan - Day 17: Outer Join Datetime Alignment Core.
    दो अलग-अलग एसेट्स के ऐतिहासिक टाइमस्टैम्प्स को बिना डेटा लीक या 
    डेटा लॉस के सिंक (Align) करता है।
    """
    # 1. explicit schemas के साथ LazyFrames को स्कैन करें (Day 16 का रीकैप)
    # मान लेते हैं कि दोनों फाइलों में 'timestamp' और 'close_price' कॉलम हैं
    asset_a_lazy = pl.scan_parquet(asset_a_path).select([
        pl.col("timestamp").cast(pl.Datetime),
        pl.col("close_price").alias("price_asset_A")
    ])
    
    asset_b_lazy = pl.scan_parquet(asset_b_path).select([
        pl.col("timestamp").cast(pl.Datetime),
        pl.col("close_price").alias("price_asset_B")
    ])
    
    # 2. Day 17 Core Architecture: Outer Join के जरिए अलाइनमेंट
    # 'how="outer"' सुनिश्चित करता है कि दोनों में से किसी भी एसेट का टाइमस्टैम्प मिस न हो
    aligned_lazy = asset_a_lazy.join(
        asset_b_lazy,
        on="timestamp",
        how="outer"
    )
    
    # 3. टाइमस्टैम्प के आधार पर क्रोनोलॉजिकल ऑर्डर (Chronological Order) में सॉर्ट करें
    # टाइम-सीरीज एनालिसिस के लिए यह स्टेप अनिवार्य है
    final_query = aligned_lazy.sort("timestamp")
    
    # 4. Lazy Context को कलेक्ट (Execute) करें
    print("[INFO] Executing optimized outer-join datetime alignment grid...")
    aligned_df = final_query.collect()
    
    return aligned_df

# --- सिमुलेशन और वेरिफिकेशन के लिए टेस्ट रन ---
if __name__ == "__main__":
    # डमी डेटा बनाकर टेस्ट करते हैं (जैसे यह असली पारके फाइल्स हों)
    # Asset A के पास 09:15 और 09:16 का डेटा है
    df_a = pl.DataFrame({
        "timestamp": [datetime(2026, 9, 9, 9, 15), datetime(2026, 9, 9, 9, 16)],
        "close_price": [100.0, 101.5]
    })
    # Asset B के पास 09:16 और 09:17 का डेटा है (09:15 मिसिंग है)
    df_b = pl.DataFrame({
        "timestamp": [datetime(2026, 9, 9, 9, 16), datetime(2026, 9, 9, 9, 17)],
        "close_price": [50.0, 50.5]
    })
    
    # इन्हें टेम्परेरी फाइल्स में सेव करते हैं
    df_a.write_parquet("asset_A.parquet")
    df_b.write_parquet("asset_B.parquet")
    
    # अलाइनमेंट फंक्शन को कॉल करें
    result_df = align_asset_datetimes("asset_A.parquet", "asset_B.parquet")
    
    print("\n--- अलाइनमेंट के बाद का रिजल्ट ग्रिड ---")
    print(result_df)
