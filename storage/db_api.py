# storage/db_api.py

import os
import asyncpg
import logging
import json
from typing import List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, dsn=None):
        self.dsn = dsn or os.environ.get("DATABASE_URL")
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=1, max_size=5)
            logger.info("Connected to the PostgreSQL database.")
        except Exception as e:
            logger.exception("Database connection failed.")
            raise

    async def close(self):
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed.")

    

    async def insert_trade(self, symbol: str, price: float, volume: float, timestamp: str | datetime, raw_message: dict = None):
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))  # Converts 'Z' to UTC-aware datetime
            if raw_message is not None and isinstance(raw_message, dict):
                raw_message = json.dumps(raw_message)
        query = """
        INSERT INTO trades (symbol, price, volume, timestamp, raw_message)
        VALUES ($1, $2, $3, $4, $5)
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(query, symbol, price, volume, timestamp, raw_message)
        except Exception as e:
            logger.exception(f"Failed to insert trade for {symbol} at {price}.")
            raise

    async def fetch_all_trades(symbol: str) -> List[Dict]:
        conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
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
