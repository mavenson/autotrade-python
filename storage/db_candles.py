# storage/db_candles.py

import asyncpg
import os
from datetime import datetime

async def save_candles_to_db(symbol: str, interval: str, source: str, candles: list[dict]):
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        for c in candles:
            ts = c["timestamp"]
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts)

            await conn.execute(
                """
                INSERT INTO candles (symbol, interval, timestamp, open, high, low, close, volume, source)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (symbol, interval, timestamp, source) DO NOTHING
                """,
                symbol, interval, ts, c["open"], c["high"], c["low"],
                c["close"], c["volume"], source
            )
    finally:
        await conn.close()


async def load_candles_from_db(symbol: str, interval: str, source: str):
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        rows = await conn.fetch(
            """
            SELECT timestamp, open, high, low, close, volume
            FROM candles
            WHERE symbol = $1 AND interval = $2 AND source = $3
            ORDER BY timestamp ASC
            """,
            symbol, interval, source
        )
    finally:
        await conn.close()

    return [
        {
            "timestamp": row["timestamp"].isoformat(),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": float(row["volume"]),
        }
        for row in rows
    ]

async def get_latest_candle_timestamp(symbol: str, interval: str, source: str):
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        row = await conn.fetchrow("""
            SELECT MAX(timestamp) as latest
            FROM candles
            WHERE symbol = $1 AND interval = $2 AND source = $3
        """, symbol, interval, source)
    finally:
        await conn.close()
    
    return row["latest"] if row and row["latest"] else None
