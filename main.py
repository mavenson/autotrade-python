# main.py

import asyncio
import signal
import logging

from storage.db_api import Database
from data.stream_builder import DataStreamBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Coinbase "match" messages
async def handle_trade_message(data, db: Database):
    if data.get("type") != "match":
        return

    try:
        await db.insert_trade(
            symbol=data["product_id"],
            price=float(data["price"]),
            volume=float(data["size"]),
            timestamp=data["time"]
        )
        logger.info(f"Saved {data['product_id']} trade at {data['price']}")
    except Exception as e:
        logger.exception(f"Insert failed: {e}")

async def run():
    db = Database()
    await db.connect()

    stream = DataStreamBuilder(
        url="wss://ws-feed.exchange.coinbase.com",
        products=["BTC-USD", "ETH-USD"]
    )

    async def wrapped_handler(data):
        await handle_trade_message(data, db)

    try:
        await stream.run(handler=wrapped_handler)
    finally:
        await db.close()
        await stream.close()

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        loop.close()

if __name__ == "__main__":
    main()