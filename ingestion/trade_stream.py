# trade_stream.py

import json
import aiohttp
import logging
from dotenv import load_dotenv

from storage.db_api import Database
from utils.message_parser import parse_trade_message

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COINBASE_WS_URL = "wss://ws-feed.exchange.coinbase.com"

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

async def run_trade_stream(db: Database):
    subscribe_msg = {
        "type": "subscribe",
        "channels": [{"name": "matches", "product_ids": ["BTC-USD", "ETH-USD"]}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(COINBASE_WS_URL) as ws:
            await ws.send_json(subscribe_msg)
            logger.info("Subscribed to Coinbase match channel.")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        if data.get("type") == "match":
                            await handle_trade_message(data, db)
                    except Exception as e:
                        logger.error(f"Error parsing WebSocket message: {e}")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {msg.data}")
                    break