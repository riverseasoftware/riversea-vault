import requests
import json
import time

# Targeted at High-Value tech launch signals
TARGET_STREAM = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_DETAIL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
WAREHOUSE_FILE = "global_gold_inventory.json"

def execute_mining():
    print("🛰️ River Sea Systems: Initiating Deep Scan...")
    try:
        signal_ids = requests.get(TARGET_STREAM, timeout=10).json()[:50]
        verified_gold = []
        gold_keywords = ["AI", "SAAS", "FUNDED", "SERIES", "RAISED", "ACQUIRED", "VC"]

        for sid in signal_ids:
            asset = requests.get(ITEM_DETAIL.format(sid)).json()
            title = asset.get('title', '').upper()
            if any(key in title for key in gold_keywords):
                verified_gold.append({
                    "asset_name": asset.get('title'),
                    "link": asset.get('url', 'Internal Signal'),
                    "intel_score": asset.get('score', 0),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        with open(WAREHOUSE_FILE, 'w') as f:
            json.dump(verified_gold, f, indent=4)
        print(f"✨ Task Finished. {len(verified_gold)} assets saved.")
    except Exception as e:
        print(f"⚠️ Warning: {e}")

if __name__ == "__main__":
    execute_mining()
