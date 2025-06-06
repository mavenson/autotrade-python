# client/services/rest_candles.py

import aiohttp
import logging
from datetime import datetime, timedelta

from storage.db_candles import save_candles_to_db
from utils.time_utils import normalize_timestamp

GRANULARITY_SECONDS = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "1h": 3600,
    "6h": 21600,
    "1d": 86400,
}

COINBASE_REST_URL = "https://api.exchange.coinbase.com"

async def fetch_rest_candles(symbol: str, interval: str, start_time=None, limit: int = 300):
    granularity = GRANULARITY_SECONDS.get(interval)
    if not granularity:
        raise ValueError(f"Unsupported interval: {interval}")


    if start_time:
        start = start_time - timedelta(seconds=granularity * 2)  # overlap 2 candles
    else:
        start = datetime.utcnow() - timedelta(seconds=granularity * limit)

    end = datetime.utcnow()
    params = {
        "start": start.isoformat(timespec="seconds") + "Z",
        "end": end.isoformat(timespec="seconds") + "Z",
        "granularity": granularity
    }

    url = f"{COINBASE_REST_URL}/products/{symbol}/candles"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception(f"REST candle request failed: {resp.status}")
            raw = await resp.json()
    
    # Validate the format
    candles = []
    for row in sorted(raw, key=lambda x: x[0]):
        if not isinstance(row, list) or len(row) != 6:
            logging.warning(f"Skipping malformed row for {symbol}: {row}")
            continue
        candles.append({
            "timestamp": normalize_timestamp(datetime.utcfromtimestamp(row[0]), granularity).isoformat() + "Z",
            "open": row[3],
            "high": row[2],
            "low": row[1],
            "close": row[4],
            "volume": row[5]
        })

    await save_candles_to_db(symbol, interval, source="rest", candles=candles)
    return candles

