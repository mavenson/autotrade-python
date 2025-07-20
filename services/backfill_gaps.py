# services/backfill_gaps.py

import asyncio
import logging
from datetime import datetime, timedelta

from client.services.candle_utils import save_rest_candles, find_missing_candle_gaps
from client.services.rest_candles import fetch_rest_candles
from storage.db_api import Database

SYMBOL = "BTC-USD"
INTERVAL = "1m"
INTERVAL_SEC = 60
LOOKBACK_HOURS = 5

logging.basicConfig(level=logging.INFO)

def batch_gap_ranges(gaps):
    """Group adjacent 1m gaps into continuous time ranges."""
    if not gaps:
        return []

    gaps.sort()
    ranges = []

    range_start, range_end = gaps[0]

    for start, end in gaps[1:]:
        if start <= range_end + timedelta(minutes=1):
            range_end = end
        else:
            ranges.append((range_start, range_end + timedelta(minutes=1)))
            range_start, range_end = start, end

    # Append the final range
    ranges.append((range_start, range_end + timedelta(minutes=1)))
    return ranges

async def backfill_once(db):
    from datetime import timezone
    """One full backfill pass within the last N hours."""
    end = datetime.utcnow().replace(second=0, microsecond=0)
    start = end - timedelta(hours=LOOKBACK_HOURS)
    cutoff = datetime.now(timezone.utc).replace(second=0, microsecond=0) - timedelta(minutes=60)
    filled_total = 0

    logging.info(f"Checking for missing {INTERVAL} candles from {start} to {end}")
    async with db.pool.acquire() as conn:
        gaps = await find_missing_candle_gaps(conn, SYMBOL, INTERVAL, start, end)

        if not gaps:
            logging.info("✅ No gaps found.")
            return False

        logging.info(f"Found {len(gaps)} missing 1m intervals. Batching...")
        ranges = batch_gap_ranges(gaps)

        for gap_range in ranges:
            range_start, range_end = gap_range

            if range_end > cutoff:
                logging.info(f"⏭️  Skipping recent gap ending at {range_end} (within freshness cutoff)")
                continue

            logging.info(f"Filling gap from {range_start} to {range_end}")
            candles = await fetch_rest_candles(SYMBOL, INTERVAL, range_start, range_end)
            await save_rest_candles(SYMBOL, INTERVAL, candles)
            filled_total += len(candles)
            logging.info(f"Saved {len(candles)} candles")

        logging.info(f"✅ Backfill complete at {datetime.utcnow().isoformat()} — {filled_total} candles saved.")
        return True

async def main():
    db = await Database.create()
    try:
        for _ in range(5):  # Limit to 5 full passes to avoid infinite looping
            had_gaps = await backfill_once(db)
            if not had_gaps:
                break
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
