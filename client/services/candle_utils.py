# client/services/candle_utils.py

import logging

from datetime import datetime, timedelta
from dateutil import parser as dtparser
from collections import defaultdict
from client.services.queries import fetch_all_trades
from client.services.rest_candles import fetch_rest_candles
from storage.db_candles import load_candles_from_db, save_candles_to_db
from utils.time_utils import floor_timestamp_to_interval


async def save_generated_candles(symbol, interval, candles):
    await save_candles_to_db(symbol, interval, source="generated", candles=candles)

async def save_rest_candles(symbol, interval, candles):
    await save_candles_to_db(symbol, interval, source="rest", candles=candles)

# Converts raw trade data into OHLCV candles bucketed by interval_seconds.
def build_candles(trades: list, interval_seconds: int) -> list:
    """Aggregate trades into OHLCV candles based on interval in seconds."""
    buckets = defaultdict(list)

    for trade in trades:
        ts = dtparser.isoparse(trade["timestamp"].isoformat() if isinstance(trade["timestamp"], datetime) else trade["timestamp"])
        bucket_start = floor_timestamp_to_interval(ts, interval_seconds)
        buckets[bucket_start].append((ts, float(trade["price"]), float(trade["volume"])))

    candles = []
    for bucket_time in sorted(buckets.keys()):
        bucket = buckets[bucket_time]
        times, prices, volumes = zip(*bucket)

        candles.append({
            "timestamp": bucket_time,
            "open": prices[0],
            "high": max(prices),
            "low": min(prices),
            "close": prices[-1],
            "volume": round(sum(volumes), 8)
        })

    return candles

# Loads candles from the DB if available; otherwise generates them (from trades or REST).
async def get_candles(symbol: str, interval: str = "1m", source: str = "generated"):
    # Step 1: Try loading from DB
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

# Detects if there are gaps in a sorted list of timestamps.
async def find_missing_candle_gaps(conn, symbol: str, interval: str, start: datetime, end: datetime, source: str = "rest", interval_sec: int = 60):
    from datetime import timezone
    start = start.replace(tzinfo=timezone.utc)
    end = end.replace(tzinfo=timezone.utc)
    result = await conn.fetch("""
        SELECT timestamp FROM candles
        WHERE symbol = $1 AND interval = $2 AND source = $3
        AND timestamp >= $4 AND timestamp <= $5
        ORDER BY timestamp
    """, symbol, interval, source, start, end)

    timestamps = [row["timestamp"] for row in result]

    if not timestamps:
        return [(start, end)]

    sorted_ts = sorted(timestamps)
    expected_gap = timedelta(seconds=interval_sec)
    gaps = []

    # Check before first known candle
    if sorted_ts[0] - start > expected_gap:
        gaps.append((start, sorted_ts[0]))

    # In between known candles
    for prev, curr in zip(sorted_ts, sorted_ts[1:]):
        if curr - prev > expected_gap:
            gaps.append((prev + expected_gap, curr))

    # After last known candle
    if end - sorted_ts[-1] > expected_gap:
        gaps.append((sorted_ts[-1] + expected_gap, end))

    return gaps


# Calls find_missing_candle_gaps() and logs human-readable messages.
def log_gaps(timestamps: list[datetime], interval_sec: int, source: str, symbol: str):
    gaps = find_missing_candle_gaps(timestamps, interval_sec)
    if gaps:
        for start, end in gaps:
            logging.warning(f"[{source.upper()}] Missing candles for {symbol}: {start} → {end}")
    else:
        logging.info(f"[{source.upper()}] No gaps detected for {symbol}")
