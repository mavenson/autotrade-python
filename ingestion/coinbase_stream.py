# ingestion/coinbase_stream.py

import json
import aiohttp
import logging
from storage.db_api import Database
from utils.message_parser import parse_trade_message

with open("config/streams.json", "r") as f:
    STREAM_CONFIG = json.load(f)

EXCHANGE_SETTINGS = STREAM_CONFIG["exchanges"]["coinbase"]
SYMBOLS = EXCHANGE_SETTINGS.get("symbols", [])
WS_URL = EXCHANGE_SETTINGS["ws_url"]

logger = logging.getLogger(__name__)

async def handle_trade_message(msg: dict, db: Database):
    try:
        trade = parse_trade_message(msg)
        await db.insert_trade(
            symbol=trade["symbol"],
            price=trade["price"],
            volume=trade["volume"],
            timestamp=trade["timestamp"],
            raw_message=msg
        )
    except Exception as e:
        logger.warning(f"Failed to handle trade message: {e}")

async def run_stream(db: Database):
    subscribe_msg = {
        "type": "subscribe",
        "channels": [{"name": "matches", "product_ids": SYMBOLS}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(WS_URL) as ws:
            await ws.send_json(subscribe_msg)
            logger.info(f"Subscribed to Coinbase match channel for: {SYMBOLS}")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        if data.get("type") == "match":
                            await handle_trade_message(data, db)
                    except Exception as e:
                        logger.error(f"WebSocket error while handling message: {e}")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket connection error: {msg.data}")
                    break

