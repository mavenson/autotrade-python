# services/gen_candle_sync.py

import asyncio
import logging
from client.services.queries import fetch_all_trades
from client.services.candle_utils import build_candles
from storage.db_candles import save_candles_to_db, get_latest_candle_timestamp

SYMBOLS = ["BTC-USD", "ETH-USD"]
INTERVALS = {
    "1m": 60,
    "5m": 300,
}
SLEEP_SECONDS = 60

logging.basicConfig(level=logging.INFO)

async def sync_once():
    for symbol in SYMBOLS:
        for interval, interval_sec in INTERVALS.items():
            try:
                latest = await get_latest_candle_timestamp(symbol, interval, source="generated")
                if latest:
                    # Go 2 buckets back to safely rebuild partial buckets
                    start_time = latest - timedelta(seconds=interval_sec * 2)
                else:
                    start_time = None

                trades = await fetch_all_trades(symbol, since=start_time)
                candles = build_candles(trades, interval_sec)
                await save_candles_to_db(symbol, interval, "generated", candles)
                logging.info(f"Saved {len(candles)} generated candles for {symbol} ({interval})")        

            except Exception as e:
                logging.error(f"Failed to build candles for {symbol} {interval}: {e}")

async def sync_loop():
    while True:
        await sync_once()
        await asyncio.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    asyncio.run(sync_loop())
