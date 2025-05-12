class PackageRsp:
    def __init__(self, rsp, stream_id):
        # user vars
        self._rsp = rsp
        self._stream_id = stream_id

        # calculated vars
        self._exchange = self._stream_id[0]
        self._prod = self._stream_id[3]
        self._channel = self._stream_id[4]

        # output vars (trades)
        self._trade_msg = None # [trade_time, trade_amt, trade_price]

        # output vars (ticker)
        self._tck_msg = None # [bid_price, bid_size, ask_price, ask_size, daily_change, daily_perc,
                             #  last_price, volume, high, low]

        # output vars (book)
        self._book_msg = None # [price_level, orders_at_price_level, total_amount_at_price_level]

    def package_bf(self):
        if type(self._rsp) == list:
            if self._channel == 'trades':
                if type(self._rsp[1]) != str:
                    pass # initial message, gives 30 last trades
                else:
                    self._trade_msg = [self._rsp[2][0], self._rsp[2][2], self._rsp[2][3]]

            elif self._channel == 'ticker':
                self._tck_msg = [self._rsp[1][0], self._rsp[1][1], self._rsp[1][2], self._rsp[1][3],
                                 self._rsp[1][4], self._rsp[1][5], self._rsp[1][6], self._rsp[1][7],
                                 self._rsp[1][8], self._rsp[1][9]]

            elif self._channel == 'book':
                if len(self._rsp[1]) > 3:
                    pass # initial message, gives 50 active book levels
                else: # regular message gives order book update when one occurs
                    self._book_msg = [self._rsp[1][0],self._rsp[1][1], self._rsp[1][2]]

    def package_cb(self):
    def package_h(self):
    def package_b(self):

    def pack(self,action):
        actions = {'cb': package_cb(), 'bf': package_bf(),'h': package_h(),'b': package_b()}
        return actions[action]

    print(stream_id)
    print(rsp)
    # ProcessRsp.check_data()