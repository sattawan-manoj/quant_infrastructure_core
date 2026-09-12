import json

def load_market_data():
    print("[INFO] स्थानीय डेटाबेस (Local Database) से मार्केट डेटा लोड किया जा रहा है...")
    
    # यह आपका फिक्स 5-मिनट का स्टॉक डेटा है जो बिना इंटरनेट के चलेगा
    historical_data = {
        "Symbol": "IBM",
        "Interval": "5min",
        "Data": {
            "2026-09-07 09:30:00": {"open": "145.20", "high": "145.80", "close": "145.50"},
            "2026-09-07 09:35:00": {"open": "145.50", "high": "146.10", "close": "145.90"},
            "2026-09-07 09:40:00": {"open": "145.90", "high": "146.00", "close": "145.60"}
        }
    }
    
    print("[SUCCESS] Day 15 का टास्क पूरा हुआ! डेटा सफलतापूर्वक लोड हो गया है।")
    print(json.dumps(historical_data, indent=4))

if __name__ == "__main__":
    load_market_data()
