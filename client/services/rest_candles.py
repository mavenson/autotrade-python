# client/services/rest_candles.py

import aiohttp
from datetime import datetime, timedelta
from storage.db_candles import save_candles_to_db

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
        start = datetime.utcnow() - timedelta(seconds=granularity * limit
                                              )
    end = datetime.utcnow()
    start = end - timedelta(seconds=granularity * limit)

    params = {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "granularity": granularity
    }

    url = f"{COINBASE_REST_URL}/products/{symbol}/candles"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception(f"REST candle request failed: {resp.status}")
            raw = await resp.json()

    # Coinbase returns: [ time, low, high, open, close, volume ]
    candles = [
        {
            "timestamp": datetime.utcfromtimestamp(row[0]).isoformat() + "Z",
            "open": row[3],
            "high": row[2],
            "low": row[1],
            "close": row[4],
            "volume": row[5]
        }
        for row in sorted(raw, key=lambda x: x[0])  # Sort by time ascending
    ]

    await save_candles_to_db(symbol, interval, source="rest", candles=candles)
    return candles
