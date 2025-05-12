# storage/db_api.py

import os
import asyncpg
import logging

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

    async def insert_trade(self, symbol: str, price: float, volume: float, timestamp: str):
        query = """
        INSERT INTO trades (symbol, price, volume, timestamp)
        VALUES ($1, $2, $3, $4)
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(query, symbol, price, volume, timestamp)
        except Exception as e:
            logger.exception(f"Failed to insert trade for {symbol} at {price}.")
            raise