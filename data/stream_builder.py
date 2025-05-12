# data/stream_builder.py

import aiohttp
import asyncio
import json
import logging

class DataStreamBuilder:
    def __init__(self, url: str, products: list[str]):
        self.url = url
        self.products = products
        self.session = None
        self.ws = None
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(self.url)
        await self.subscribe()

    async def subscribe(self):
        msg = json.dumps({
            "type": "subscribe",
            "channels": [{
                "name": "matches",
                "product_ids": self.products
            }]
        })
        await self.ws.send_str(msg)
        self.logger.info(f"Subscribed to: {self.products}")

    async def receive_messages(self, handler):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                await handler(data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                self.logger.error("WebSocket error")
                break

    async def run(self, handler):
        try:
            await self.connect()
            await self.receive_messages(handler)
        finally:
            await self.close()

    async def close(self):
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()