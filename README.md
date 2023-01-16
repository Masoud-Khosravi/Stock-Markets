<div align="center">

# Import data from $\color{#AE00DD} Stock \space Markets$  and $\color{#00BC3C}Trade$ in it

![GitHub last commit](https://img.shields.io/github/last-commit/Masoud-Khosravi/Stock-Markets)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/Masoud-Khosravi/Stock-Markets)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Masoud-Khosravi/Stock-Markets)

# $\color{red}Hello \space \color{lightblue}and \space \color{orange}Wellcome$


</div>

## In this Package we try input data and trade in stock markets base on $\color{#00D4FF}Metatrader5$
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
<br/>

## Other Repositories:
[![Readme Card](https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username=masoud-khosravi&repo=SQL-Python)](https://github.com/Masoud-Khosravi/SQL-Python)
[![Readme Card](https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username=masoud-khosravi&repo=Tensorflow-Covid-19)](https://github.com/Masoud-Khosravi/Tensorflow-Covid-19)

[![Readme Card](https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username=masoud-khosravi&repo=Machine-Learning)](https://github.com/Masoud-Khosravi/Machine-Learning)
[![Readme Card](https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username=masoud-khosravi&repo=Stock-Markets)](https://github.com/Masoud-Khosravi/Stock-Markets)

[![Readme Card](https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username=masoud-khosravi&repo=Sqlite)](https://github.com/Masoud-Khosravi/Sqlite)
[![Readme Card](https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username=masoud-khosravi&repo=Docker)](https://github.com/Masoud-Khosravi/Docker)

<br/>
<br/>
<div align="left">

## $\color{red}About \space \color{orange}Me:$
<a href="https://github.com/Masoud-Khosravi">
  <img src="https://user-images.githubusercontent.com/121137036/210107231-0ae2f150-bb07-4e53-a2e2-a006b9b799e4.gif" alt="drawing" style="width:600px;"/>
</a>
<br/>
<br/>

</div>
<p align="center">
  <br/>
  <a href="https://www.linkedin.com/in/masoudkhosravi/">
      <img src="https://img.shields.io/badge/-Linkedin-blue?style=flat-square&logo=linkedin">
  </a>
  <a href="mailto:masoudkh.new@gmail.com">
      <img src="https://img.shields.io/badge/-Email-red?style=flat-square&logo=gmail&logoColor=white">
    <a href="https://hub.docker.com/r/masoudnew/sqlite">
      <img src="https://img.shields.io/badge/-Docker-blue?style=flat-square&logo=Docker&logoColor=white">
  </a>
  <a href="https://github.com/Masoud-Khosravi">
     <img src="https://komarev.com/ghpvc/?username=masoud-khosravi&label=Visitors&color=0e75b6&style=flat" alt="Masoud-Khosravi" />
  </a>
  <br/>
  <a href="https://github.com/Masoud-Khosravi">
      <img src="https://github-stats-alpha.vercel.app/api?username=masoud-khosravi&cc=22272e&tc=37BCF6&ic=fff&bc=0000" /> 
  <!---  
      <img src="https://github-readme-stats.vercel.app/api?username=masoud-khosravi&show_icons=true&hide=issues,contribs&theme=react&hide_border=true" />
  -->
    
  </a>
  
</p>
