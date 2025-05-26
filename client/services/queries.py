# client/services/queries.py

import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def fetch_trade_counts():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("""
        SELECT symbol, COUNT(*) AS trade_count
        FROM trades
        GROUP BY symbol
        ORDER BY trade_count DESC;
    """)
    await conn.close()
    return rows

async def fetch_date_ranges():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("""
        SELECT symbol,
               MIN(timestamp) AS start_time,
               MAX(timestamp) AS end_time
        FROM trades
        GROUP BY symbol
        ORDER BY symbol;
    """)
    await conn.close()
    return rows

async def fetch_all_trades(symbol: str):
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("""
        SELECT symbol, price, volume, timestamp
        FROM trades
        WHERE symbol = $1
        ORDER BY timestamp ASC;
    """, symbol)
    await conn.close()

    return [
        {
            "symbol": row["symbol"],
            "price": str(row["price"]),
            "volume": str(row["volume"]),
            "timestamp": row["timestamp"].isoformat(),
        }
        for row in rows
    ]
