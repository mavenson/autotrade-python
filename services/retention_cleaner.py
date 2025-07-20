# storage/retention_cleaner.py

import asyncio
import argparse
from datetime import datetime, timedelta
from storage.db_api import Database

# Define retention per exchange
RETENTION_POLICIES = {
    "coinbase": 60,   # days
    "binance": 10     # days
}

async def enforce_retention(exchange: str = None):
    db = await Database.create()
    try:
        async with db.pool.acquire() as conn:
            now = datetime.utcnow()

            exchanges = [exchange] if exchange else RETENTION_POLICIES.keys()

            for ex in exchanges:
                days = RETENTION_POLICIES.get(ex)
                if days is None:
                    print(f"⚠️  Unknown exchange: {ex}")
                    continue
                cutoff = now - timedelta(days=days)
                result = await conn.execute(
                    """
                    DELETE FROM trades
                    WHERE exchange = $1 AND timestamp < $2
                    """,
                    ex,
                    cutoff
                )
                print(f"🧹 Deleted old {ex} trades — result: {result}")
    finally:
        await db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enforce retention policy on trades table.")
    parser.add_argument("--exchange", help="Limit retention cleanup to a specific exchange")
    args = parser.parse_args()

    asyncio.run(enforce_retention(exchange=args.exchange))
