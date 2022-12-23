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
    df_type1_changed = None
    df_last_candle_raw = None
    df_last_candle_type1 = None
    df_last_candle_type1_changed = None
    _Mt5 = Mt5
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
        symbols = self._Mt5.symbols_get()
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
            self.df_type1_changed = self._get_data_type1_changed(self.df_type1_raw)
            self.df_last_candle_type1_changed = self._get_data_type1_changed_last_candle()
            return True
        except Exception as err:
            print("ERR :", err)
            return False

    # @property
    def update_last(self) -> bool:
        try:
            self.df_last_candle_type1_changed = self._get_data_type1_changed_last_candle()
            return True
        except Exception as err:
            print(err)
            return False

    def _get_raw_data(self, start_pos, count):
        df = self._Mt5.copy_rates_from_pos(self.symbol, self.time_frame, start_pos,
                                           count)  # 2 Days=2818 -- 2740+52+26 ->3D=4188  in Alpari in others 1 day=1380
        df = pd.DataFrame(df)
        # convert time in seconds into the datetime format
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.drop(['spread', 'real_volume'], axis=1)
        return df

    @staticmethod
    def _get_data_type1(dataframe_raw):
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
        df = df.dropna()
        df = df.reset_index(drop=True)
        return df

    def _get_data_type1_changed(self, dataframe_type1_raw):
        df = dataframe_type1_raw.copy()
        ##########
        point = self._Mt5.symbol_info(self.symbol).point

        def dest(num1, num2):
            return (num1 - num2) / point

        # Calculate All Distance From Close by point
        df['open'] = np.vectorize(dest)(df['close'], df['open'])
        df['high'] = np.vectorize(dest)(df['close'], df['high'])
        df['low'] = np.vectorize(dest)(df['close'], df['low'])
        df['Low9'] = np.vectorize(dest)(df['close'], df['Low9'])
        df['Low26'] = np.vectorize(dest)(df['close'], df['Low26'])
        df['Low52'] = np.vectorize(dest)(df['close'], df['Low52'])
        df['High9'] = np.vectorize(dest)(df['close'], df['High9'])
        df['High26'] = np.vectorize(dest)(df['close'], df['High26'])
        df['High52'] = np.vectorize(dest)(df['close'], df['High52'])

        # We Use only Time (not date) and convert every candle time to minute of day -->  Hour*60 +minute
        df['time'] = df['time'].apply(lambda num: num.hour * 60 + num.minute)

        # Close Distance from Close is equal 0 -->
        df = df.drop(['close'], axis=1)

        # Scaling All Dataframe
        scaler = StandardScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
        self._scaler = scaler
        return df

    def _get_data_type1_changed_last_candle(self):
        df_raw = self._get_raw_data(1, 53)
        self.df_last_candle_raw = df_raw[-1:]

        df = self._get_data_type1(df_raw)
        self.df_last_candle_type1 = df.copy()
        ##########
        point = self._Mt5.symbol_info(self.symbol).point

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

        # We Use only Time (not date) and convert every candle time to minute of day -->  Hour*60 +minute
        df['time'] = df['time'].apply(lambda num: num.hour * 60 + num.minute)

        # Close Distance from Close is equal 0 -->
        df = df.drop(['close'], axis=1)

        # Use Scaler Before Created in class
        scaler = self._scaler
        df = pd.DataFrame(scaler.transform(df), columns=df.columns)
        return df

    ####################################################################################################################
    def _str_to_timeframe(self, argument="M1"):
        switcher = {
            "M1": self._Mt5.TIMEFRAME_M1,
            "M2": self._Mt5.TIMEFRAME_M2,
            "M3": self._Mt5.TIMEFRAME_M3,
            "M4": self._Mt5.TIMEFRAME_M4,
            "M5": self._Mt5.TIMEFRAME_M5,
            "M6": self._Mt5.TIMEFRAME_M6,
            "M10": self._Mt5.TIMEFRAME_M10,
            "M12": self._Mt5.TIMEFRAME_M12,
            "M15": self._Mt5.TIMEFRAME_M15,
            "M20": self._Mt5.TIMEFRAME_M20,
            "M30": self._Mt5.TIMEFRAME_M30,
            "H1": self._Mt5.TIMEFRAME_H1,
            "H2": self._Mt5.TIMEFRAME_H2,
            "H3": self._Mt5.TIMEFRAME_H3,
            "H4": self._Mt5.TIMEFRAME_H4,
            "H6": self._Mt5.TIMEFRAME_H6,
            "H8": self._Mt5.TIMEFRAME_H8,
            "H12": self._Mt5.TIMEFRAME_H12,
            "D": self._Mt5.TIMEFRAME_D1,
            "W": self._Mt5.TIMEFRAME_W1,
            "MN": self._Mt5.TIMEFRAME_MN1,
        }
        return switcher.get(argument, False)

# End Of Class MetaTrader
