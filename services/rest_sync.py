# services/rest_sync.py
#Periodically fetches recent candles from a REST API (e.g. Coinbase), normalizes them, stores them in DB.

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

GRANULARITY_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "1d": 86400,
}

logging.basicConfig(level=logging.INFO)


async def sync_once():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                logging.info(f"Pulling REST candles: {symbol} {interval}")
                latest = await get_latest_candle_timestamp(symbol, interval, source="rest")

                interval_sec = GRANULARITY_SECONDS.get(interval, 60)
                start_time = latest - timedelta(seconds=interval_sec) if latest else None

                candles = await fetch_rest_candles(symbol, interval, start_time=start_time)

                if not candles:
                    logging.info(f"No new candles for {symbol} ({interval})")
                    continue

                await save_candles_to_db(symbol, interval, source="rest", candles=candles)

                timestamps = [dtparser.isoparse(c["timestamp"]) for c in candles]
                log_gaps(timestamps, interval_sec, source="rest", symbol=symbol)

                logging.info(f"Saved {len(candles)} candles for {symbol} ({interval})")
                await asyncio.sleep(0.5)  # throttle API calls

            except Exception as e:
                logging.error(f"Failed to sync {symbol} {interval}: {e}")

if __name__ == "__main__":
    asyncio.run(sync_once())
