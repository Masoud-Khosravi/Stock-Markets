import pandas as pd


class TradeOnMeta:
    import MetaTrader5 as Mt5
    symbol = None
    volume = float(0.1)
    order_type = 0
    price = 0
    sl = float(0)
    tp = float(0)
    deviation = 20
    magic = int(12345)
    comment = str("Python Trade")
    _Mt5 = Mt5
    _action = Mt5.TRADE_ACTION_DEAL
    _type_time = Mt5.ORDER_TIME_GTC
    _type_filling = Mt5.ORDER_FILLING_FOK
    _is_close = False
    _pos_id = 0
    _request = ""

    def __init__(self):
        self.AllowTrade = False
        self.Enter = self._Mt5.initialize()
        if not self.Enter:
            print("initialize() failed")
            self._Mt5.shutdown()
        else:
            self.terminal_info()

    def __bool__(self):
        return self.Enter and self.AllowTrade

    def terminal_info(self) -> dict:
        if self.Enter:
            res = self._Mt5.terminal_info()
            if res is not None and res != ():
                terminal_info_dict = res._asdict()
                self.AllowTrade = terminal_info_dict['trade_allowed']
                # df_terminal = pd.DataFrame(list(terminal_info_dict.items()), columns=['property', 'value'])
                return terminal_info_dict

        return dict()  # This Line returns an empty data

    def __iter__(self):
        if self._is_close:
            yield from {
                "action": self._action,
                "symbol": self.symbol,
                "volume": self.volume,
                "type": self.order_type,
                "price": self.price,
                "position": int(self._pos_id),
                "deviation": self.deviation,
                "magic": self.magic,
                "comment": self.comment,
                "type_time": self._type_time,
                "type_filling": self._type_filling
            }.items()
        else:
            yield from {
                "action": self._action,
                "symbol": self.symbol,
                "volume": self.volume,
                "type": self.order_type,
                "price": self.price,
                "sl": self.sl,
                "tp": self.tp,
                "deviation": self.deviation,
                "magic": self.magic,
                "comment": self.comment,
                "type_time": self._type_time,
                "type_filling": self._type_filling
            }.items()

    def __dict__(self):
        return {
            "action": self._action,
            "symbol": self.symbol,
            "volume": self.volume,
            "type": self.order_type,
            "price": self.price,
            "sl": self.sl,
            "tp": self.tp,
            "deviation": self.deviation,
            "magic": self.magic,
            "comment": self.comment,
            "type_time": self._type_time,
            "type_filling": self._type_filling
        }

    def is_symbol_exist(self):
        find = False
        symbols = self._Mt5.symbols_get()
        for item in symbols:
            if item.name == self.symbol:
                find = True
                break
        return find

    def positions_get(self) -> pd.DataFrame():
        if self.symbol is None:
            res = self._Mt5.positions_get()
        else:
            res = self._Mt5.positions_get(symbol=self.symbol)

        if res is not None and res != ():
            df = pd.DataFrame(list(res), columns=res[0]._asdict().keys())
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df

        return pd.DataFrame()  # This Line returns an empty data

    def _send_order_request(self) -> bool:
        result = self._Mt5.order_send(self._request)
        if result is None:
            print("ERROR: Somthing Wrong, request:\n", self._request)
            return False
        elif result.retcode == self._Mt5.TRADE_RETCODE_DONE:
            print("Done.\nTicket={}, volume={}, price={}, symbol={}".format(result.order, result.volume,
                                                                            result.request.price,
                                                                            result.request.symbol))
            return result
        else:
            print("ERR : ", result)
            return False

    def order_send(self, symbol, order_type, lot=0.01, sl=0.0, tp=0.0, deviation=20, magic=123455,
                   comment="Python Trade") -> bool:
        """
            OrderType: 'Buy' Or 'Sell'
        """
        self._is_close = False
        self.comment = "Python Send Order"
        self.symbol = symbol
        is_exist = self.is_symbol_exist()
        self._action = self._Mt5.TRADE_ACTION_DEAL
        self.volume = float(lot)
        if is_exist:
            if order_type.lower() == 'buy':
                price = self._Mt5.symbol_info_tick(symbol).ask
                order_type = self._Mt5.ORDER_TYPE_BUY
            elif order_type.lower() == 'sell':
                price = self._Mt5.symbol_info_tick(symbol).bid
                order_type = self._Mt5.ORDER_TYPE_SELL
            else:
                raise TypeError("The order_type Should be 'Buy' or 'Sell")
        else:
            raise NameError("The Symbols name << {} >> is not exist in MT5 symbols".format(symbol))
        self.order_type = order_type
        self.price = price
        self.sl = float(sl)
        self.tp = float(tp)
        self.deviation = deviation
        self.magic = int(magic)
        self.comment = str(comment)
        self._type_time = self._Mt5.ORDER_TIME_GTC
        self._type_filling = self._Mt5.ORDER_FILLING_FOK
        self._request = dict(self)
        # send a trading request
        return self._send_order_request()

    def close_position(self, deal_id) -> bool:
        open_position = self.positions_get()
        open_position = open_position[open_position['ticket'] == deal_id].reset_index(drop=True)
        if len(open_position) == 0:
            print("ERR : Position By Ticket {} Not Found".format(deal_id))
            return False
        self.order_type = open_position["type"][0]
        self.symbol = open_position['symbol'][0]
        self.volume = open_position['volume'][0]
        if self.order_type == self._Mt5.ORDER_TYPE_BUY:
            self.order_type = self._Mt5.ORDER_TYPE_SELL
            self.price = self._Mt5.symbol_info_tick(self.symbol).bid
        else:
            self.order_type = self._Mt5.ORDER_TYPE_BUY
            self.price = self._Mt5.symbol_info_tick(self.symbol).ask
        self.comment = "Close by Python"
        self._is_close = True
        self._pos_id = deal_id
        self._request = dict(self)
        return self._send_order_request()

    def close_sells(self, symbol=None) -> bool:
        self.symbol = symbol
        open_positions = self.positions_get()
        err = False
        for pos in range(0, len(open_positions)):
            if open_positions["type"][pos] != self._Mt5.ORDER_TYPE_SELL:
                continue
            self._pos_id = open_positions["ticket"][pos]
            self.symbol = open_positions['symbol'][pos]
            self.volume = open_positions['volume'][pos]
            self.order_type = self._Mt5.ORDER_TYPE_BUY
            self.price = self._Mt5.symbol_info_tick(self.symbol).ask
            self.comment = "Close All Sells"
            self._is_close = True
            self._request = dict(self)
            result = self._send_order_request()
            if not result:
                err = True
        return not err

    def close_buys(self, symbol=None) -> bool:
        self.symbol = symbol
        open_positions = self.positions_get()
        err = False
        for pos in range(0, len(open_positions)):
            if open_positions["type"][pos] != self._Mt5.ORDER_TYPE_BUY:
                continue
            self._pos_id = open_positions["ticket"][pos]
            self.symbol = open_positions['symbol'][pos]
            self.volume = open_positions['volume'][pos]
            self.order_type = self._Mt5.ORDER_TYPE_SELL
            self.price = self._Mt5.symbol_info_tick(self.symbol).bid
            self.comment = "Close All Buys"
            self._is_close = True
            self._request = dict(self)
            result = self._send_order_request()
            if not result:
                err = True
        return not err

    def close_all(self, symbol=None) -> bool:
        self.symbol = symbol
        open_positions = self.positions_get()
        err = False
        for pos in range(0, len(open_positions)):
            self._pos_id = open_positions["ticket"][pos]
            self.symbol = open_positions['symbol'][pos]
            self.volume = open_positions['volume'][pos]
            self.order_type = open_positions["type"][pos]
            if self.order_type == self._Mt5.ORDER_TYPE_BUY:
                self.order_type = self._Mt5.ORDER_TYPE_SELL
                self.price = self._Mt5.symbol_info_tick(self.symbol).bid
            else:
                self.order_type = self._Mt5.ORDER_TYPE_BUY
                self.price = self._Mt5.symbol_info_tick(self.symbol).ask
            self.comment = "Close all orders"
            self._is_close = True
            self._request = dict(self)
            result = self._send_order_request()
            if not result:
                err = True
        return not err

    def positions_total_buy(self, symbol=None):
        self.symbol = symbol
        open_positions = self.positions_get()
        all_buys = 0
        for pos in range(0, len(open_positions)):
            order_type = open_positions["type"][pos]
            if order_type == self._Mt5.ORDER_TYPE_BUY:
                all_buys += 1
        return all_buys

    def positions_total_sell(self, symbol=None):
        self.symbol = symbol
        open_positions = self.positions_get()
        all_sells = 0
        for pos in range(0, len(open_positions)):
            order_type = open_positions["type"][pos]
            if order_type == self._Mt5.ORDER_TYPE_SELL:
                all_sells += 1
        return all_sells
