# services/gen_candle_sync.py

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
import argparse

from storage.db_api import Database
from client.services.candle_utils import build_candles, save_generated_candles

SYMBOL = os.getenv("SYMBOL", "BTC-USD")
INTERVAL = os.getenv("INTERVAL", "1m")
INTERVAL_SEC = 60

logging.basicConfig(level=logging.INFO)

async def ensure_indexes(conn):
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol)")
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp)")

async def delete_existing_candles(conn):
    logging.info(f"[FULL] Clearing existing generated candles for {SYMBOL}")
    await conn.execute("""
        DELETE FROM candles
        WHERE symbol = $1 AND interval = $2 AND source = 'generated'
    """, SYMBOL, INTERVAL)

async def get_trade_time_bounds(conn):
    result = await conn.fetchrow("""
        SELECT MIN(timestamp) AS start, MAX(timestamp) AS end
        FROM trades
        WHERE symbol = $1
    """, SYMBOL)
    return result['start'], result['end']

async def sync_hour(conn, start_time, end_time):
    query = """
        SELECT * FROM trades
        WHERE symbol = $1 AND timestamp >= $2 AND timestamp < $3
        ORDER BY timestamp
    """
    rows = await conn.fetch(query, SYMBOL, start_time, end_time)
    logging.info(f"[{start_time.isoformat()}] Retrieved {len(rows)} trades")
    candles = build_candles(rows, INTERVAL_SEC)
    await save_generated_candles(SYMBOL, INTERVAL, candles)
    logging.info(f"[{start_time.isoformat()}] Saved {len(candles)} candles")

async def run_full_sync(db, clean=False):
    async with db.pool.acquire() as conn:
        await ensure_indexes(conn)
        if clean:
            await delete_existing_candles(conn)
        start, end = await get_trade_time_bounds(conn)
        if not start or not end:
            logging.warning("No trades found to generate candles.")
            return

        curr = start.replace(minute=0, second=0, microsecond=0)
        while curr < end:
            await sync_hour(conn, curr, curr + timedelta(hours=1))
            curr += timedelta(hours=1)

async def run_recent_sync(db):
    async with db.pool.acquire() as conn:
        await ensure_indexes(conn)
        lookback = datetime.utcnow() - timedelta(minutes=5)
        cutoff = datetime.utcnow().replace(second=0, microsecond=0)

        query = """
            SELECT * FROM trades
            WHERE symbol = $1 AND timestamp >= $2 AND timestamp < $3
            ORDER BY timestamp
        """
        rows = await conn.fetch(query, SYMBOL, lookback, cutoff)

        logging.info(f"Building generated candles: {SYMBOL} {INTERVAL}")
        if not rows:
            logging.info("No complete trades found for recent sync. Skipping.")
            return

        candles = build_candles(rows, INTERVAL_SEC)
        await save_generated_candles(SYMBOL, INTERVAL, candles)
        logging.info(f"Saved {len(candles)} candles")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="Generate candles from all trades (historical)")
    parser.add_argument("--clean", action="store_true", help="Clear existing generated candles first")
    args = parser.parse_args()

    db = await Database.create()
    try:
        if args.full:
            await run_full_sync(db, clean=args.clean)
        else:
            await run_recent_sync(db)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
