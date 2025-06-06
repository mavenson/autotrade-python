# client/services/candle_utils.py

import datetime
from dateutil import parser as dtparser
from collections import defaultdict
from client.services.queries import fetch_all_trades
from client.services.rest_candles import fetch_rest_candles
from storage.db_candles import load_candles_from_db, save_candles_to_db


def floor_timestamp_to_interval(ts: datetime.datetime, interval: int) -> datetime.datetime:
    """Round down timestamp to nearest interval (in seconds)."""
    return ts - datetime.timedelta(seconds=ts.timestamp() % interval)

def build_candles(trades: list, interval_seconds: int) -> list:
    """Aggregate trades into OHLCV candles based on interval in seconds."""
    buckets = defaultdict(list)

    for trade in trades:
        ts = dtparser.isoparse(trade["timestamp"])
        bucket_start = floor_timestamp_to_interval(ts, interval_seconds)
        buckets[bucket_start].append((ts, float(trade["price"]), float(trade["volume"])))

    candles = []
    for bucket_time in sorted(buckets.keys()):
        bucket = buckets[bucket_time]
        times, prices, volumes = zip(*bucket)

        candles.append({
            "timestamp": bucket_time.isoformat(),
            "open": prices[0],
            "high": max(prices),
            "low": min(prices),
            "close": prices[-1],
            "volume": round(sum(volumes), 8)
        })

    return candles

async def get_candles(symbol: str, interval: str = "1m", source: str = "generated"):
    #S Step 1: Try loading from DB
    candles = await load_candles_from_db(symbol, interval, source)
    if candles:
        return candles

    # Step 2: Fallback
    if source == "generated":
        trades = await fetch_all_trades(symbol)

        # Convert interval string to seconds
        interval_seconds_map = {
            "1m": 60,
            "5m": 300,
            "15m": 900,
            "1h": 3600,
            "1d": 86400
        }
        interval_seconds = interval_seconds_map.get(interval)
        if not interval_seconds:
            raise ValueError(f"Unsupported interval: {interval}")

        candles = build_candles(trades, interval_seconds)
        await save_candles_to_db(symbol, interval, "generated", candles)
        return candles
    elif source == "rest":
        candles = await fetch_rest_candles(symbol, interval)
        return candles
    else:
        raise ValueError(f"Unknown candle source: {source}")
