# services/rest_sync.py

import asyncio
import logging
from client.services.rest_candles import fetch_rest_candles
from storage.db_candles import save_candles_to_db, get_latest_candle_timestamp
import datetime

SYMBOLS = ["BTC-USD", "ETH-USD"]
INTERVALS = ["1m", "5m"]
SLEEP_SECONDS = 60  # how often to run

logging.basicConfig(level=logging.INFO)

async def sync_once():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                logging.info(f"Pulling REST candles: {symbol} {interval}")
                latest = await get_latest_candle_timestamp(symbol, interval, source="rest")
                candles = await fetch_rest_candles(symbol, interval, start_time=latest)
                await save_candles_to_db(symbol, interval, source="rest", candles=candles)
                logging.info(f"Saved {len(candles)} candles for {symbol} ({interval})")
            except Exception as e:
                logging.error(f"Failed to sync {symbol} {interval}: {e}")

async def sync_loop():
    while True:
        await sync_once()
        await asyncio.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    asyncio.run(sync_loop())
