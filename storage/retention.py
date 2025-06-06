# storage/retention.py

import asyncio
import os
from storage.db_api import Database

RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", 60))

async def enforce_retention():
    db = await Database.create()
    try:
        query = f"""
            DELETE FROM trades
            WHERE timestamp < NOW() - INTERVAL '{RETENTION_DAYS} days';
        """
        async with db.pool.acquire() as conn:
            result = await conn.execute(query)
            print(f"Retention cleanup result: {result}")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(enforce_retention())
