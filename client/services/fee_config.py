# client/services/fee_config.py

import json
import os

CONFIG_PATH = os.path.join("config", "exchanges.json")

def load_exchange_fees(exchange: str) -> dict:
    try:
        with open(CONFIG_PATH, "r") as f:
            fee_data = json.load(f)
        return fee_data.get(exchange.lower())
    except Exception as e:
        print(f"Error loading exchange fee config: {e}")
        return None
