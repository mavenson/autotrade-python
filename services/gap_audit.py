# services/gap_audit.py
import asyncio
import json
import logging
import os
from datetime import datetime
from storage.db_candles import load_candles_from_db
from client.services.candle_utils import find_missing_candle_gaps, log_gaps

# Ensure logs directory exists
os.makedirs("/home/ubuntu/autotrade-python/logs", exist_ok=True)

# Configure logging
log_file = "/home/ubuntu/autotrade-python/logs/gap_audit.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Load stream config
with open("config/streams.json") as f:
    config = json.load(f)

active_exchange = config["active_exchange"]
exchange_settings = config["exchanges"][active_exchange]
symbols = exchange_settings.get("symbols", [])
intervals_from_config = exchange_settings.get("intervals", ["1m"])
INTERVALS = {interval: 60 for interval in intervals_from_config}

async def run_audit():
    for symbol in symbols:
        for interval, interval_sec in INTERVALS.items():
            try:
                candles = await load_candles_from_db(symbol, interval, source="generated")
                timestamps = [datetime.fromisoformat(c["timestamp"].replace("Z", "")) for c in candles]
                log_gaps(timestamps, interval_sec, source="generated", symbol=symbol)
            except Exception as e:
                logging.error(f"Gap audit failed for {symbol} {interval}: {e}")

if __name__ == "__main__":
    asyncio.run(run_audit())
