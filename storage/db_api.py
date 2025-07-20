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
        self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=1, max_size=5)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def insert_trade(self, symbol, price, volume, timestamp, raw_message=None, exchange="coinbase"):
        query = """
        INSERT INTO trades (symbol, price, volume, timestamp, raw_message, exchange)
        VALUES ($1, $2, $3, $4, $5, $6)
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, symbol, price, volume, timestamp, raw_message, exchange)

    @classmethod
    async def create(cls):
        instance = cls()
        await instance.connect()
        return instance
