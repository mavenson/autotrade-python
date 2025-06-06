# services/rest_sync.py

import json
import asyncio
import logging
from client.services.rest_candles import fetch_rest_candles
from client.services.candle_utils import log_gaps
from storage.db_candles import save_candles_to_db, get_latest_candle_timestamp
from datetime import datetime, timedelta
from dateutil import parser as dtparser


with open("config/streams.json") as f:
    STREAM_CONFIG = json.load(f)

ACTIVE_EXCHANGE = STREAM_CONFIG["active_exchange"]
EXCHANGE_SETTINGS = STREAM_CONFIG["exchanges"][ACTIVE_EXCHANGE]

SYMBOLS = EXCHANGE_SETTINGS.get("symbols", [])
INTERVALS = EXCHANGE_SETTINGS.get("intervals", ["1m"])

SLEEP_SECONDS = 60  # how often to run

logging.basicConfig(level=logging.INFO)

async def sync_once():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                logging.info(f"Pulling REST candles: {symbol} {interval}")
                latest = await get_latest_candle_timestamp(symbol, interval, source="rest")
                
                if latest:
                    interval_sec = 60 if interval == "1m" else 300
                    start_time = latest - timedelta(seconds=interval_sec)
                else:
                    start_time = None

                candles = await fetch_rest_candles(symbol, interval, start_time=latest)
                
                if not candles:
                    logging.info(f"No new candles for {symbol} ({interval})")
                    continue

                await save_candles_to_db(symbol, interval, source="rest", candles=candles)

                timestamps = [dtparser.isoparse(c["timestamp"]) for c in candles]
                interval_sec = 60 if interval == "1m" else 300
                log_gaps(timestamps, interval_sec, source="rest", symbol=symbol)
                
                logging.info(f"Saved {len(candles)} candles for {symbol} ({interval})")
                await asyncio.sleep(0.5) # throttle API calls

            except Exception as e:
                logging.error(f"Failed to sync {symbol} {interval}: {e}")

async def sync_loop():
    while True:
        await sync_once()
        await asyncio.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    asyncio.run(sync_loop())
