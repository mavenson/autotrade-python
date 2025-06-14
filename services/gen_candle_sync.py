# services/gen_candle_sync.py
# Periodically fetches trades from DB, generates synthetic candles using build_candles, and stores them in DB.

import json
import asyncio
import logging
from client.services.queries import fetch_all_trades
from client.services.candle_utils import build_candles, log_gaps
from storage.db_candles import save_candles_to_db, get_latest_candle_timestamp
from datetime import timedelta
from dateutil import parser as dtparser


with open("config/streams.json") as f:
    config = json.load(f)
SYMBOLS = config["exchanges"][config["active_exchange"]]["symbols"]
INTERVALS = {interval: 60 for interval in EXCHANGE_SETTINGS.get("intervals", ["1m"])}

logging.basicConfig(level=logging.INFO)


async def sync_once():
    for symbol in SYMBOLS:
        for interval, interval_sec in INTERVALS.items():
            try:
                latest = await get_latest_candle_timestamp(symbol, interval, source="generated")
                start_time = latest - timedelta(seconds=interval_sec * 2) if latest else None

                trades = await fetch_all_trades(symbol, since=start_time)
                candles = build_candles(trades, interval_sec)

                await save_candles_to_db(symbol, interval, "generated", candles)

                timestamps = [c["timestamp"] for c in candles]
                log_gaps(timestamps, interval_sec, source="generated", symbol=symbol)


                logging.info(f"Saved {len(candles)} generated candles for {symbol} ({interval})")

            except Exception as e:
                logging.error(f"Failed to build candles for {symbol} {interval}: {e}")




if __name__ == "__main__":
    asyncio.run(sync_once())
