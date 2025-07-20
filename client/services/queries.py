# client/services/queries.py

import asyncpg
import os
import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

async def fetch_trade_counts():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("""
        SELECT symbol, COUNT(*) AS count
        FROM trades
        GROUP BY symbol
        ORDER BY symbol ASC
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

async def fetch_all_trades(symbol: str, since: datetime.datetime = None, exchange: str = None):
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        base_query = """
            SELECT symbol, price, volume, timestamp
            FROM trades
            WHERE symbol = $1
        """
        params = [symbol]

        if exchange:
            base_query += " AND exchange = $2"
            params.append(exchange)

        if since:
            base_query += f" AND timestamp >= ${len(params)+1}"
            params.append(since)

        base_query += " ORDER BY timestamp ASC"

        rows = await conn.fetch(base_query, *params)

    finally:
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
