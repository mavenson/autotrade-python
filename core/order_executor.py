import datetime

# With user input, Order class generates other data fields with various functions.
# TradeBook offers functions to Create, Cancel, and Modify Orders in addition to storing
# pertinent order data (max number of orders disp at once) in class variables and the db. Will also
# keep permanent record of full order history in db.

gset_trade_mode = 'Manual'  # Manual/Auto
gset_last_id = 0  # Would normally pull something like this from database

class Order:
    def __init__(self, type=None, side=None, prod=None, amt=None, exe_prc=None, exch=None, trg=None, channel=None):
        # Data from Arguments:
        self._type = type # Limit/Market/StopLoss/BuyAbvMrkt/Trailing
        self._side = side # Is order to ultimately buy or sell
        self._prod = prod # What product is the order for
        self._amt = amt # What's the amount to be bought/sold
        self._exe_prc = exe_prc # at what price is the order set to execute
        self._exch = exch # What exchange is the order with/for
        self._trg = trg # Does this order trigger any other orders on completion? order id?
        self._channel = channel
        # Calculated Data:
        self._id = None
        self._status = None # Can be Active, Cancelled, Filled, Partially Filled
        self._plc_by = None # calls global setting
        self._tm_plc = None # saves to current time when order is generated
        self._tm_snc_plc = None # time since order placed
        # Data Calculated on Order Execution
        self._exe_list = [] # Default empty list, when any executions, append to list in given instance
        self._exe_tm = None # Time of last execution
        self._tm_snc_exe = None  # Time since execution
        self._tm_to_exe = None  # Time between order placement and execution
        self._exe_agg = None # aggregates average price per unit when executed at different prices (mkt order)
        self._filled = None
        self._amt_lft = None
        self._dict_obj = {}

    def update_dict(self):
        # Dictionary object representing order
        self._tm_snc_plc = str(self.time_delta(self.curr_time(), self._tm_plc))
        self._dict_obj = {
                          'type': self._type, 'side': self._side, 'prod': self._prod, 'amt': self._amt,
                          'exe_prc': self._exe_prc, 'exch': self._exch,'trg': self._trg,
                          'id': self._id, 'channel': self._channel, 'status': self._status, 'plc_by': self._plc_by, 'tm_plc': self._tm_plc.strftime('%Y-%m-%d %H:%M:%S.%f'),
                          'tm_snc_plc': self._tm_snc_plc, 'exe_list': self._exe_list, 'exe_tm': self._exe_tm,
                          'tm_snc_exe': self._tm_snc_exe, 'tm_to_exe': self._tm_to_exe, 'exe_agg': self._exe_agg,
                          'filled': self._filled, 'amt_lft': self._amt_lft
                         }

    def curr_time(self):
        result = datetime.datetime.now()
        return result

    def time_delta(self,t1,t2):
        result = t1 - t2
        return result

    def gen_vars(self):
        global gset_last_id
        gset_last_id += 1
        self._id = str(gset_last_id).zfill(6)
        self._status = 'Active' # Can be Active, Cancelled, Filled, Partially Filled
        self._plc_by = gset_trade_mode # calls global setting
        self._tm_plc = self.curr_time() # saves to current time when order is generated

    def add_exe(self,amt,prc):
        self._exe_list.append([amt, prc, self.curr_time()])

    def gen_exe_vars(self):
        self._exe_tm = self._exe_list[-1][-1]  # Time of last execution
        self._tm_snc_exe =  datetime.datetime.now() - self._exe_tm # Time since execution
        self._tm_to_exe = self._exe_tm - self._tm_plc # Time between order placement and execution
        self._exe_agg =  sum([(e[0] / sum(v[0] for v in self._exe_list)) * e[1] for e in self._exe_list])
                       # Default as None, aggregates average price paid per unit if executed at different prices
        self._filled = sum([v[0] for v in self._exe_list]) # Default as externally set amt, update on partial execution, if One shot set to 0
        self._amt_lft =  self._amt - self._filled # Displays amount left to be filled
        if self._filled > 0 and self._amt_lft > 0:
            self._status = 'Partially Filled'
        elif self._amt_lft == 0:
            self._status = 'Filled'

    def ld_exst_ord(self,dict_obj):
        for e in dict_obj:
            self._dict_obj[e] = dict_obj[e]

    def return_dict(self):
        return self._dict_obj

class OrderManager:
    def __init__(self):
        self._order_dock = {}
        self.ld_ord_dock()

    def ld_ord_dock(self):
        pass # Pull list of dict_objects from database. POSTGRES

    # def ld_ord_frm_dict_obj(self, dict_obj):
    #     order = Order()
    #     order.ld_exst_ord(dict_obj)
    #     if order._exe_list:
    #         order.gen_exe_vars()
    #     self.add_to_dock(order)

    def create_new_order(self, type, side, prod, amt, prc, exch, trg, chnl):
        order = Order(type, side, prod, amt, prc, exch, trg, chnl)
        order.gen_vars()
        order.update_dict()
        self.add_to_dock(order)

    def modify_order(self, id, price, amt):
        print(self._order_dock)
        for e in self._order_dock:
            if e == id:
                self._order_dock[e]._exe_prc = price
                self._order_dock[e]._amt = amt

    def cancel_order(self, id):
        self._order_dock[id]._status = 'Cancelled'

    def add_to_dock(self, order):
        order_id = order.return_dict()['id']
        self._order_dock[order_id] = order

    def rm_from_dock(self, id):
        for i in list(self._order_dock):
            if i == id:
                del self._order_dock[i]

    def exe_updt(self,order,exe_info):
        order.add_exe(exe_info)
        order.gen_exe_vars()

    def save_orders(self):
        None # Merge the current order list with the database, check for redundancy POSTGRES

    def launch_disp(self):
        None # Launch separate class to create wxpython window display with current_orders data. WXPYTHON

    def test_display(self): # Temporary non-wxpython order readout for development purposes.
        while True:
                print('\n')
                selection = input("1. Display Active Orders\n2. Test Execution\n3. Test Cancel Order\
                \n4. Test Modify Order\n5. Test Remove Order From Dock\n\nEnter Selection: ")
                if selection == '1':
                    for e in self._order_dock:
                        print('\n')
                        self._order_dock[e].update_dict()
                        order_dict = self._order_dock[e].return_dict()
                        for i in order_dict:
                            print('%s: %s' %(i, order_dict[i]))
                elif selection == '2':
                    self._order_dock['000002'].add_exe(.2, 297)
                    self._order_dock['000002'].gen_exe_vars()
                    self._order_dock['000002'].add_exe(.1, 292)
                    self._order_dock['000002'].gen_exe_vars()
                    self._order_dock['000002'].add_exe(.05, 276)
                    self._order_dock['000002'].gen_exe_vars()
                elif selection == '3':
                    self.cancel_order('000001')
                elif selection == '4':
                    self.modify_order('000002', 350, .3)
                elif selection == '5':
                    self.rm_from_dock('000001')


class ProcessRsp:
    def __init__(self):
        self._last_rsp = None
        self._active_orders = {}

    def ld_actv_ords(self,order_dock):
        for e in order_dock:
            if e['status'] == 'Active' or e['status'] == 'Partially Filled':
                self._active_orders[e] = order_dock[e]

    def check_data(self, rsp):
        self._last_rsp = rsp
        for e in self._active_orders:
            if  e['stream_id'] == rsp['stream_id']:
                if e['exe_prc'] == rsp['prc']:
                    Execute.mkt_order(e)
                    e.modify_order(e, 'status', 'Pending')

# class ExchAcctInfo():
#     def __init__(self):

    # Depending on whether a websocket feed can provide needed data or if it must be API polled as fast as
    # possible
    # this must listen for order status updates provided by exchanges and modify tracked orders appropriately

class Execute():
    def __init__(self):
        pass
    def mkt_order(self,order):
        pass

if __name__ == '__main__':
    order_man = OrderManager()
    order_man.create_new_order('Limit', 'Buy', 'btc-usd', .1, 6500, 'bf', None, 'ticker')
    order_man.create_new_order('Stop', 'Sell', 'eth-usd', .5, 300, 'cb', None, 'ticker')
    order_man.test_display()


# It would be good to include only information pertinent to Executor in the active_orders list_item format



