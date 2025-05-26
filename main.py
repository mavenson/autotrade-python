# main.py

import asyncio
from storage.db_api import Database
from ingestion.trade_stream import run_trade_stream

async def main():
    db = Database()
    await db.connect()
    try:
        await run_trade_stream(db)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
