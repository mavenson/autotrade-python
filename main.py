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
        tasks.append(DataStreamBuilder(session, wrapped[0], wrapped[1], wrapped[2]).open_link())
    await asyncio.wait(tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())