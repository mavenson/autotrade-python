# main.py

import asyncio
import json
from storage.db_api import Database

with open("config/streams.json", "r") as f:
    config = json.load(f)

active_exchange = config["active_exchange"]

if active_exchange == "coinbase":
    from ingestion.coinbase_stream import run_stream
else:
    raise NotImplementedError(f"Exchange '{active_exchange}' not supported yet.")

async def main():
    db = await Database.create()
    try:
        await run_stream(db)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
