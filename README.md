# inputs data from Stock Markets and Trade in it
## In this Package we try input data and trade in stock markets base on Metatrader5
(for Now and later maybe we add other options )

#
## Using this Package is too easy:
+ Befor use you should--> [pip install MetaTrader5](https://pypi.org/project/MetaTrader5/)

+ and you Should [install MT5](https://www.metatrader5.com/en/download) on your PC and create acount(free and easy)

Now -->
just add libraries next to your code and simply use it    
Example (ReadData):
    
```python
from ReadData import MetaTrader
my_obj = MetaTrader("XAUUSD", "M1",start_pos=1, count=500)
# Get Last 500 candels data From timeframe M1 and symbol 'XAUUSD'
df=my_obj.df_raw # This is a Pandas Dataframe
df.head()
```

Example (Trade):
```python
from Trade import TradeOnMeta
MT=TradeOnMeta()
df=MT.positions_total_buy("XAUUSD")
# Get get all buy positions from symbol 'XAUUSD' --> Pandas Dataframe
df.head()
```

# under development ...
## < we will come back soon >