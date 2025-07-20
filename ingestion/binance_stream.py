# ingestion/binance_stream.py

import json
import aiohttp
from datetime import datetime
from storage.db_api import Database
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
SYMBOL = "BTCUSDT"  # Binance uses uppercase with no dash
WS_URL = f"wss://stream.binance.us:9443/ws/{SYMBOL.lower()}@trade"

async def handle_trade_message(msg: dict, db: Database):
    try:
        ts = datetime.utcfromtimestamp(msg["T"] / 1000)  # 'T' = trade time in ms
        trade = {
            "symbol": SYMBOL,
            "price": float(msg["p"]),     # price
            "volume": float(msg["q"]),    # quantity
            "timestamp": ts,
        }
        await db.insert_trade(
            symbol=trade["symbol"],
            price=trade["price"],
            volume=trade["volume"],
            timestamp=trade["timestamp"],
            raw_message=json.dumps(msg),
            exchange="binance"
        )
        logger.info(f"[Binance] Saved trade @ {trade['price']} ({trade['volume']}) at {trade['timestamp']}")
        logger.debug(f"[Binance] Raw trade message: {msg}")
    except Exception as e:
        logger.warning(f"[Binance] Failed to handle trade message: {e}")

async def run_stream(db: Database):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(WS_URL) as ws:
            logger.info(f"[Binance] Connected to {WS_URL}")
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    logger.info(f"[Binance] Received raw WS message")
                    try:
                        data = json.loads(msg.data)
                        await handle_trade_message(data, db)
                    except Exception as e:
                        logger.error(f"[Binance] Error processing message: {e}")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"[Binance] WebSocket connection error: {msg.data}")
                    break

if __name__ == "__main__":
    import asyncio
    import os
    from storage.db_api import Database

    async def main():
        db = await Database.create()
        try:
            await run_stream(db)
        finally:
            await db.close()

    asyncio.run(main())
