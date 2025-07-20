# main.py

import asyncio
from storage.db_api import Database
from ingestion.coinbase_stream import run_stream as run_coinbase


#        with open("config/streams.json", "r") as f:
#            config = json.load(f)

async def main():
    db = await Database.create()
    try:
        await run_coinbase(db)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
