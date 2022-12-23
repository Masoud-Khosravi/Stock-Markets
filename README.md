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
my_obj = MetaTrader("XAUUSD", "M1",start_pos=1, count=200)
# Get Last 200 candles data From timeframe M1 and symbol 'XAUUSD'
df=my_obj.df_raw # This is a Pandas Dataframe
df.head()
```
![df_raw](img/df_raw.png)

## we have 3 type of datafram
+ df_raw
+ df_raw_type1   --> this df has Low9,Low26,Low52 and High9,High26,high52
+ df_type1_changed --> this is normalized and scaled data from df_raw_type1

Here is df_raw_type1:
![df_raw_type1](img/df_raw_type1.png)

and this is df_type1_changed:
![df_type1_changed](img/df_type1_changed.png)


and also we can use
```python
my_obj.update() # This function will update the databases  
my_obj.update_last() # This function will update only last databases  
```
## After we use our dataframes (for example in sklearn) now we need only last candles data and they here-->
```python
my_obj.update_last()
my_obj.df_last_candle_raw
```
![df_lastcandle_raw](img/df_lastcandle_raw.png)
```
my_obj.df_last_candle_type1
```
![df_lastcandle_type1](img/df_lastcandle_type1.png)
```
my_obj.df_last_candle_type1_changed
```
![df_lastcandle_type1_changed](img/df_lastcandle_type1_changed.png)

#
# Now its time to visualizing data
## this part is easy too -->

```python
from Visualize import plot_line,plot_candlestick
plot_line(my_obj.df_raw) # its done :D
```
![plot_line](img/plot_line.png)

```python
plot_candlestick(my_obj.df_raw)
```
![plot_candlestick](img/plot_candlestick.png)


#
# Now its time To Trade:

## class trade has many fanctions like:
+ order_send
+ close_position
+ close_sells
+ close_buys
+ close_all
+ positions_total
+ positions_total_buy
+ positions_total_sell
+ terminal_info

## Example of using Trade:

Example (Trade):
```python
from Trade import TradeOnMeta
MT=TradeOnMeta()
df=MT.positions_total_buy("XAUUSD")
# Get get all buy positions from symbol 'XAUUSD' --> Pandas Dataframe
MT.close_all("BITCOIN") # Close All positions in 'BITCOIN'
MT.order_send("BITCOIN",'Buy',lot=0.25, sl=12000, tp=20000) # Open Trade in 'BITCOIN'
MT.close_sells()# Close All sell position from all symbols
...
```
#
### under development ...
* < we will come back soon >