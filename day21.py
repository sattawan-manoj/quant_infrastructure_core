import polars as pl

# 1. अपनी फाइल का रास्ता तय करें
cache_path = "./quant_apprenticeship/data_feed/macro_assets_5y.parquet"

print("--- 🏛️ MY MINI QUANT DATABASE ---")

# 2. फाइल को सीधे लोड करें
df = pl.read_parquet(cache_path)

# 3. स्क्रीन पर ऊपर की 5 लाइनें प्रिंट करें
print("\n🔍 [DATA PREVIEW] ऊपर की 5 लाइनें:")
print(df.head(5))

# 4. चेक करें कि डेटा पूरी तरह साफ है या नहीं
null_sum = sum([df[col].null_count() for col in df.columns])
print(f"\n✅ [QUALITY CHECK] बची हुई कुल Null वैल्यूज: {null_sum}")
