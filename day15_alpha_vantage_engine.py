import os
import requests
import time

# =====================================================================
# 🏛️ DAY 15: DATA INGESTION ENGINE (DECOUPLED)
# =====================================================================
# Rule: This file only downloads data. It knows NOTHING about trading.
# =====================================================================

class DataDownloader:
    def __init__(self, api_key: str = "demo"):
        """
        Initializes our downloader. We use the free 'demo' key from Alpha Vantage.
        The demo key only works for a few symbols like 'IBM'.
        """
        self.api_key = api_key
        self.url = "https://alphavantage.co"

    def fetch_daily_data(self, symbol: str, folder_path: str):
        """
        Downloads historical stock data from the internet and saves it as a CSV file.
        """
        # Safety Check: If the storage folder doesn't exist on your computer, make it!
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"📁 [FOLDER CREATED] Created new folder at: {folder_path}")

        # The parameters required by the Alpha Vantage website to give us data
        parameters = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "full",  # 'full' gets 5+ years of daily data
            "datatype": "csv",     # We want it as a text CSV file
            "apikey": self.api_key
        }

        print(f"🌐 [NETWORK] Connecting to internet to download data for: {symbol}...")
        
        # Make the actual internet request
        response = requests.get(self.url, params=parameters)

        # Basic verification: Did the internet connection fail?
        if response.status_code != 200:
            print(f"❌ [ERROR] Internet connection failed. Status: {response.status_code}")
            return

        # Simple file name generation (e.g., IBM_raw_data.csv)
        file_name = f"{symbol}_raw_data.csv"
        final_save_path = os.path.join(folder_path, file_name)

        # Open a new file on your hard drive and save the text inside it
        with open(final_save_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"📦 [SUCCESS] Saved historical records to: {final_save_path}")

# =====================================================================
# 🏃‍♂️ RUNTIME TEST ENVIRONMENT (How we test our work)
# =====================================================================
if __name__ == "__main__":
    # Define where we want to save our raw files
    STORAGE_DIRECTORY = "./quant_apprenticeship/data_feed/raw_vault/"
    
    # Initialize our downloader tool
    downloader = DataDownloader(api_key="demo")
    
    # Let's test it by downloading historical data for IBM
    start_clock = time.time()
    
    downloader.fetch_daily_data(symbol="IBM", folder_path=STORAGE_DIRECTORY)
    
    end_clock = time.time()
    total_time = end_clock - start_clock
    print(f"⏱️ Done! The download took {total_time:.2f} seconds.")
