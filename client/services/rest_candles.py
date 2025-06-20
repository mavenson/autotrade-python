# client/services/rest_candles.py

import aiohttp
import logging
import json
from datetime import datetime, timedelta

from storage.db_candles import save_candles_to_db
from utils.time_utils import normalize_timestamp

# Load config
with open("config/streams.json") as f:
    STREAM_CONFIG = json.load(f)

ACTIVE_EXCHANGE = STREAM_CONFIG["active_exchange"]
SYMBOLS = STREAM_CONFIG["exchanges"][ACTIVE_EXCHANGE]["symbols"]

# Coinbase API details
COINBASE_REST_URL = "https://api.exchange.coinbase.com"

GRANULARITY_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "6h": 21600,
    "1d": 86400,
}

async def fetch_rest_candles(symbol: str, interval: str, start_time=None, limit: int = 300):
    granularity = GRANULARITY_SECONDS.get(interval)
    if not granularity:
        raise ValueError(f"Unsupported interval: {interval}")

    # Build time window
    if start_time:
        start = start_time - timedelta(seconds=granularity * 2)  # overlap to avoid gaps
    else:
        start = datetime.utcnow() - timedelta(seconds=granularity * limit)
    end = datetime.utcnow()

    params = {
        "start": start.isoformat(timespec="seconds") + "Z",
        "end": end.isoformat(timespec="seconds") + "Z",
        "granularity": granularity,
    }

    url = f"{COINBASE_REST_URL}/products/{symbol}/candles"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception(f"REST candle request failed: {resp.status}")
            try:
                raw = await resp.json()
            except Exception as e:
                raise Exception(f"Failed to parse JSON from REST: {e}")

    candles = []
    valid_rows = [row for row in raw if isinstance(row, list) and len(row) == 6]
    for row in sorted(valid_rows, key=lambda x: x[0]):
        candles.append({
            "timestamp": normalize_timestamp(datetime.utcfromtimestamp(row[0]), granularity).isoformat() + "Z",
            "open": row[3],
            "high": row[2],
            "low": row[1],
            "close": row[4],
            "volume": row[5],
        })

    for row in raw:
        if not isinstance(row, list) or len(row) != 6:
            logging.warning(f"Skipping malformed row for {symbol}: {row}")

    await save_candles_to_db(symbol, interval, source="rest", candles=candles)
    return candles

