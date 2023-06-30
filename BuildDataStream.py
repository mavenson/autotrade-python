import json
import aiohttp
import asyncio
import gzip

class EchoWebSocket:
    def __init__(self, cli_session, ws_link, rqst_msg, stream_id):
        self._rqst_msg = rqst_msg
        self._ws_link = ws_link
        self._cli_session = cli_session
        self._ws = None
        self._ws_connect = None
        self._stream_id = stream_id

    async def open_link(self):
        async with self._cli_session.ws_connect(self._ws_link) as self._ws:
            print(self._rqst_msg)
            if self._rqst_msg == None:
                async for msg in self._ws:
                    msg_dc = json.loads(msg.data)
                    package_rsp(msg_dc, self._stream_id)
            elif self._ws_link[10:15] == 'huobi':
                await self._ws.send_str(self._rqst_msg)
                async for msg in self._ws:
                    msg_dc = json.loads(gzip.decompress(msg.data).decode('utf-8'))
                    if 'ping' in msg_dc:
                        pong = str(msg_dc['ping'])
                        await self._ws.send_str(pong)
                        await self._ws.send_str(self._rqst_msg)
                    else:
                        package_rsp(msg_dc, self._stream_id)
            else:
                await self._ws.send_str(self._rqst_msg)
                async for msg in self._ws:
                    msg_dc = json.loads(msg.data)
                    package_rsp(msg_dc, self._stream_id)

    async def close_link(self):
        await self._ws.close()

    async def db_daemon(self):
        None


def rqst_wrapper(user_rqst):
    wrapping = {
                     'bf': ["wss://api.bitfinex.com/ws/2",
                    {"event":"subscribe", "channel": None, "symbol": None}],

                     'cb': ['wss://ws-feed.pro.coinbase.com',
                    {'type':'subscribe', 'product_ids': None,'channels': None}],

                     'h': ['wss://api.huobi.pro/ws',
                    {'sub': None, 'id': None}],

                     'b': ['wss://stream.binance.com:9443/ws/', None]
               }
    for e in wrapping:
        if e == user_rqst[0]:
            url = wrapping[e][0]
            rqst = wrapping[e][1]
            stream_id = [user_rqst[0], user_rqst[1], user_rqst[3]]
            if e == 'bf':
                rqst['channel'], rqst['symbol'] = user_rqst[1], user_rqst[2]
                return [url, json.dumps(rqst), stream_id]
            elif e == 'cb':
                rqst['channels'], rqst['product_ids'] = [user_rqst[1]], [user_rqst[2]]
                return [url, json.dumps(rqst), stream_id]
            elif e == 'h':
                rqst['sub'], rqst['id'] = user_rqst[1], user_rqst[2]
                return [url, json.dumps(rqst), stream_id]
            elif e == 'b':
                return [url+str(user_rqst[1]), None, stream_id]

def package_rsp(rsp, stream_id):
    # Needs to determine where data is from and format it in a universal way for ProcessRsp to input
    # Make Sure to Generate a Stream ID following a deducible convention such as 'cb-btcusd'
    # logic to format response message from websocket for given exchange:
    print(stream_id)
    print(rsp)

    # ProcessRsp.check_data()
    # Call PackageRsp Class


async def main():
    session = aiohttp.ClientSession()
    rqst_list_demo = [
                      # ['bf', 'trades', 'tBTCUSD', 'btc-usd', 'trades'],
                      # ['bf', 'ticker', 'tBTCUSD','btc-usd','ticker'],
                      # ['bf', 'book', 'tBTCUSD', 'btc-usd','book'],
                      ['cb', 'full', 'BTC-USD', 'btc-usd','full']
                      # ['h', 'market.ethbtc.kline.1min', 'id63', 'h-btcusd'],
                      # ['b', 'ltcbtc@trade', None, 'b-btcusd']
                     ]
    tasks = []
    for e in rqst_list_demo:
        wrapped = rqst_wrapper(e)
        tasks.append(EchoWebSocket(session, wrapped[0], wrapped[1], wrapped[2]).open_link())
    await asyncio.wait(tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


# {"sub": "market.ethbtc.kline.1min","id": "id63"}