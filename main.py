# main.py

import asyncio
from storage.db_api import Database
from trade_stream import run_trade_stream

async def main():
    db = await Database.create()
    try:
        await run_trade_stream(db)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())