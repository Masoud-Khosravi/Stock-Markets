import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


####################################################################################################################
class MetaTrader:
    import MetaTrader5 as Mt5
    if not Mt5.initialize():
        print("initialize() failed")
        Mt5.shutdown()

    symbol = None
    time_frame = ""
    df_raw = None
    df_type1_raw = None
    df_type1_final = None
    df_last_candle_type1 = None
    sl_sell = 0.0
    tp_sell = 0.0
    sl_buy = 0.0
    tp_buy = 0.0
    _scaler = None
    _start_pos = 1
    _count = 2818
    _symbol_exist = False

    # price=0

    def __init__(self, symbol, timeframe="M1", start_pos=1, count=2818):
        """
        TimeFrame: "M1","M2","M3","M4","M5","M6","M10,"M12","M15,"M20","M30"
                   "H1","H2","H3","H4","H6","H8","H12"
                   "D" , "W" , "MN"
        """
        self._start_pos = start_pos
        self._count = count
        self.time_frame = self._str_to_timeframe(timeframe)
        self.symbol = symbol
        self._symbol_exist = self._is_symbol_exist()
        if self:
            self.update()

    def __bool__(self):
        return self._symbol_exist and bool(self.time_frame)

    def _is_symbol_exist(self):
        find = False
        symbols = Mt5.symbols_get()
        for item in symbols:
            if item.name == self.symbol:
                find = True
                break
        return find

    # @property
    def update(self) -> bool:
        try:
            self.df_raw = self._get_raw_data(self._start_pos, self._count)
            self.df_type1_raw = self._get_data_type1(self.df_raw)
            self.df_type1_final = self._get_data_type1_changed(self.df_type1_raw)
            self.df_last_candle_type1 = self._get_data_type1_changed_last_candle()
            return True
        except Exception as err:
            print("ERR :", err)
            return False

    # @property
    def update_last(self) -> bool:
        try:
            self.df_last_candle_type1 = self._get_data_type1_changed_last_candle()
            return True
        except Exception as err:
            print(err)
            return False

    def _get_raw_data(self, start_pos, count):
        df = Mt5.copy_rates_from_pos(self.symbol, self.time_frame, start_pos,
                                     count)  # 2 Days=2818 -- 2740+52+26 ->3D=4188  in Alpari in others 1 day=1380
        df = pd.DataFrame(df)
        # convert time in seconds into the datetime format
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.drop(['spread', 'real_volume'], axis=1)
        return df

    def _get_data_type1(self, dataframe_raw, is_last=False):
        df = dataframe_raw.copy()
        df.insert(len(df.columns), 'High9', np.nan)
        df.insert(len(df.columns), 'High26', np.nan)
        df.insert(len(df.columns), 'High52', np.nan)
        df.insert(len(df.columns), 'Low9', np.nan)
        df.insert(len(df.columns), 'Low26', np.nan)
        df.insert(len(df.columns), 'Low52', np.nan)
        for row in np.arange(52, len(df)):
            df.loc[row, 'High9'] = np.amax(df.loc[row - 8:row, 'high'])
            df.loc[row, 'High26'] = np.amax(df.loc[row - 25:row, 'high'])
            df.loc[row, 'High52'] = np.amax(df.loc[row - 51:row, 'high'])
            df.loc[row, 'Low9'] = np.amin(df.loc[row - 8:row, 'low'])
            df.loc[row, 'Low26'] = np.amin(df.loc[row - 25:row, 'low'])
            df.loc[row, 'Low52'] = np.amin(df.loc[row - 51:row, 'low'])
            # ========== End For
        df['time'] = df['time'].apply(lambda num: num.hour)
        df = df.dropna()
        df = df.reset_index(drop=True)
        if not is_last:
            ###################
            point = Mt5.symbol_info(self.symbol).point

            def dest(num1, num2):
                return (num1 - num2) / point

            ###################
            df.insert(len(df.columns), 'BS', np.nan)
            for pos in np.arange(0, len(df)):
                close_price = df.loc[pos, 'close']
                sl_buy = dest(close_price, df.loc[pos, 'Low26'])
                if sl_buy < 75:
                    sl_buy = 75
                sl_sell = dest(df.loc[pos, 'High26'], close_price)
                if sl_sell < 75:
                    sl_sell = 75
                tp_buy = sl_buy * 2.1
                tp_sell = sl_sell * 2.1
                signal = 0
                if (df.loc[pos, 'time'] < 23) and (df.loc[pos, 'time'] > 4):
                    for last in np.arange(1, 25):
                        if (pos + last) < len(df):
                            high_last = dest(df.loc[pos + last, 'High26'], close_price)
                            low_last = dest(close_price, df.loc[pos + last, 'Low26'])
                            low_now = dest(close_price, df.loc[pos + last, 'low'])
                            high_now = dest(df.loc[pos + last, 'high'], close_price)
                            if (low_last <= sl_buy) and (high_now > tp_buy):
                                signal = 1
                                break
                            elif (high_last <= sl_sell) and (low_now > tp_sell):
                                signal = 2
                                break
                df.loc[pos, 'BS'] = signal
            # End of for pos in np.arrange(0,len(df)):
            df = df.iloc[:-26, :]
        # End of  if(not isLast):
        return df

    def _get_data_type1_changed(self, dataframe_type1):
        df = dataframe_type1.drop('BS', axis=1)
        ##########
        point = Mt5.symbol_info(self.symbol).point

        def dest(num1, num2):
            return (num1 - num2) / point

        #########
        df['open'] = np.vectorize(dest)(df['close'], df['open'])
        df['high'] = np.vectorize(dest)(df['close'], df['high'])
        df['low'] = np.vectorize(dest)(df['close'], df['low'])
        df['Low9'] = np.vectorize(dest)(df['close'], df['Low9'])
        df['Low26'] = np.vectorize(dest)(df['close'], df['Low26'])
        df['Low52'] = np.vectorize(dest)(df['close'], df['Low52'])
        df['High9'] = np.vectorize(dest)(df['close'], df['High9'])
        df['High26'] = np.vectorize(dest)(df['close'], df['High26'])
        df['High52'] = np.vectorize(dest)(df['close'], df['High52'])
        ######
        df = df.drop(['close'], axis=1)
        scaler = StandardScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
        # print(df.head())
        df['BS'] = dataframe_type1['BS']
        self._scaler = scaler
        return df

    def _get_data_type1_changed_last_candle(self):
        df_raw = self._get_raw_data(1, 53)
        df = self._get_data_type1(df_raw, is_last=True)
        # print(df.head())
        ##########
        point = Mt5.symbol_info(self.symbol).point

        def dest(num1, num2):
            return (num1 - num2) / point

        #########
        price = df['close'][0]
        self.sl_buy = df['Low26'][0]
        self.sl_sell = df['High26'][0]
        self.tp_buy = price + (price - self.sl_buy) * 2
        self.tp_sell = price - (self.sl_sell - price) * 2
        df['open'] = np.vectorize(dest)(df['close'], df['open'])
        df['high'] = np.vectorize(dest)(df['close'], df['high'])
        df['low'] = np.vectorize(dest)(df['close'], df['low'])
        df['Low9'] = np.vectorize(dest)(df['close'], df['Low9'])
        df['Low26'] = np.vectorize(dest)(df['close'], df['Low26'])
        df['Low52'] = np.vectorize(dest)(df['close'], df['Low52'])
        df['High9'] = np.vectorize(dest)(df['close'], df['High9'])
        df['High26'] = np.vectorize(dest)(df['close'], df['High26'])
        df['High52'] = np.vectorize(dest)(df['close'], df['High52'])
        # =============
        df = df.drop(['close'], axis=1)
        scaler = self._scaler
        df = pd.DataFrame(scaler.transform(df), columns=df.columns)
        return df

    ####################################################################################################################
    # @staticmethod
    def _str_to_timeframe(self, argument="M1"):
        switcher = {
            "M1": Mt5.TIMEFRAME_M1,
            "M2": Mt5.TIMEFRAME_M2,
            "M3": Mt5.TIMEFRAME_M3,
            "M4": Mt5.TIMEFRAME_M4,
            "M5": Mt5.TIMEFRAME_M5,
            "M6": Mt5.TIMEFRAME_M6,
            "M10": Mt5.TIMEFRAME_M10,
            "M12": Mt5.TIMEFRAME_M12,
            "M15": Mt5.TIMEFRAME_M15,
            "M20": Mt5.TIMEFRAME_M20,
            "M30": Mt5.TIMEFRAME_M30,
            "H1": Mt5.TIMEFRAME_H1,
            "H2": Mt5.TIMEFRAME_H2,
            "H3": Mt5.TIMEFRAME_H3,
            "H4": Mt5.TIMEFRAME_H4,
            "H6": Mt5.TIMEFRAME_H6,
            "H8": Mt5.TIMEFRAME_H8,
            "H12": Mt5.TIMEFRAME_H12,
            "D": Mt5.TIMEFRAME_D1,
            "W": Mt5.TIMEFRAME_W1,
            "MN": Mt5.TIMEFRAME_MN1,
        }
        return switcher.get(argument, False)

####################################################################################################################

# my_class = ReadDataMetatrader("XAUUSD", "M1")
# if my_class:
#     print("Everything is fine.")
# else:
#     print("Entered Symbol <{}> is {}".format(my_class.symbol, my_class._symbol_exist))
#     print("and Entered Timeframe is {}".format(my_class.time_frame))
#
# my_class.update
# df = my_class.df_type1_final
# print(df.head())
# print("=======================")
# last = my_class.df_last_candle_type1
# print(last.head())
