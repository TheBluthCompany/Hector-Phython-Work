#!/usr/bin/env python
# coding: utf-8

# In[12]:


#invite all of our frendz

import numpy as np
import talib as talib
import yfinance as yf
import pandas as pandas
import matplotlib
import matplotlib.pyplot as plt


# In[13]:


#download our USD/SEK dataset

df = yf.download("SPY")

df


# In[14]:


#calculate or simple moving averages

close_price = df['Close']
sma50 = close_price.rolling(50).mean()
sma200 = close_price.rolling(200).mean()

plt.plot(sma50) #blue
plt.plot(sma200) #orange

#bullish to bearish, and vice-versa, causes direction to change and slopes to hit. 

#maybe, for you, there's a tomorrow. there's 1,000, 3,000, 10,000; but for some of us, there's only today...


# In[16]:


print("The difference between the third, and second, day of trading are as follows:", close_price.iloc[3] - close_price.iloc[2])

print(close_price.iloc[4])
print(close_price.iloc[3])


print(10.5598-10.6295)


# In[19]:


#begin the SMA crossover trading strategy

plt.plot(sma50)
plt.plot(sma200)


# In[20]:


#loop that provides us with price data over time, and our trading signals

entry = None #remember, for the very first time, there isn't an entry price to calculate. We use "None". 
PnLs = []
dates = []
for i in range(len(close_price)):
    if i >= 50:
        if ((sma50.loc[sma50.index[i-1], "SPY"] > sma200.loc[sma200.index[i-1], "SPY"])) and ((sma50.loc[sma50.index[i], "SPY"] < sma200.loc[sma200.index[i], "SPY"])):
            if entry:
                PnL = (((entry - close_price.loc[close_price.index[i], "SPY"]) / entry)* 100)
                print(f'SHORT on {close_price.index[i]}, PnL is: {PnL}')
                PnLs.append(PnL)
                dates.append(close_price.index[i])

            entry = close_price.loc[close_price.index[i], "SPY"]
            
            
            
        elif ((sma50.loc[sma50.index[i-1], "SPY"] < sma200.loc[sma200.index[i-1], "SPY"])) and ((sma50.loc[sma50.index[i], "SPY"] > sma200.loc[sma200.index[i], "SPY"])):
            if entry:
                PnL = ((close_price.loc[close_price.index[i], "SPY"] - entry) / entry ) *100
                print(f'LONG on {close_price.index[i]}, PnL is: {PnL}')
                PnLs.append(PnL)
                dates.append(close_price.index[i])
                
            entry = close_price.loc[close_price.index[i], "SPY"]
print(np.cumprod(PnLs))
plt.plot(dates, np.cumprod(PnLs)) #We're using np.cumsum() because we want to show a rolling sum of our PnL's, 
                                 #instead of just every single PnL scattered around. plt.plot(x_axis, y_axis)
    


# In[27]:





# In[31]:


close_price.loc[close_price.index[1], "SPY"]


# In[32]:


#Let's visualize then the Sep'24 Death Cross was hit

plt.plot(sma50.loc['1998-09-01 00:00:00': "1998-12-25 00:00:00" , "SPY"])
plt.plot(sma200.loc['1998-09-01 00:00:00': "1998-12-25 00:00:00" , "SPY"])


# In[33]:


close_price.loc[close_price.index[8000], 'SPY']


# In[159]:


'''Strategy Outline
Use moving averages (MA) to identify trends. For example:
Buy USD/SEK when the short-term MA (e.g., 20-day) crosses above the long-term MA (e.g., 50-day).
Sell USD/SEK when the short-term MA crosses below the long-term MA.
Include an ATR (Average True Range) filter to ensure you only trade during higher volatility periods.

Backtest over a 5-year horizon using daily price data.
Your First Task:
Get the Data: Pull USD/SEK daily historical data for the last 5 years. You can use sources like Yahoo Finance (yfinance), Bloomberg, or any API you prefer.
Clean the Data: Ensure timestamps are uniform, and handle missing data (interpolation or drop).
Plot the Data: Plot USD/SEK's daily close to understand trends and volatility over time.
Once you’ve got that, send me the code or results, and we’ll layer on the moving average strategy next. How does that sound?

#position sizes? 
Got it! Let’s go with volatility-adjusted sizing using ATR to determine position size. This way, you’re adjusting for market conditions and ensuring that during higher volatility (when ATR is larger), you’re taking smaller positions, and during low volatility, you're able to take larger positions. It’s a more adaptive approach that ensures consistent risk management across varying market environments.

Here’s how we could structure it:

Risk per trade: Let’s say we risk 1% of total equity per trade.
Position size: Position size = (Risk per trade) / (ATR * Stop-Loss distance in SEK).
This gives us a dynamic sizing model that adjusts depending on the volatility of the USD/SEK pair.

How does that sound to you?

'''
#The average volatility range for the Dollar Krona is 0.93% - trade in times where vol > 93% & SMA's cross. 

import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
import matplotlib
import yfinance as yf
import datetime

print(datetime.date.today())

#Environment-specifics
initial_aum = 600000000
risk_per_trade = 600000000 * 0.01
one_lot = 100000
margin = 2.00

#Dataframes & Data-to-use
    #Timeframe:
horizon = datetime.timedelta(365*5) #5-year horizon

    #Dataframe
USDSEK_df = yf.download("USDSEK=X", datetime.date.today()-horizon,datetime.date.today())
USDSEK_Close_Price = USDSEK_df['Close']

    #Moving Averages
sma20 = USDSEK_Close_Price.rolling(20).mean()      #blue
sma100 = USDSEK_Close_Price.rolling(100).mean()    #orange

    #Calculating our ATR
highs = []
lows = []
closes = []
ticker = "USDSEK=X"

for i in range(len(USDSEK_df)):
    highs.append(USDSEK_df["High"].loc[USDSEK_df['High'].index[i], "USDSEK=X"])
    lows.append(USDSEK_df["Low"].loc[USDSEK_df["Low"].index[i], "USDSEK=X"])
    closes.append(USDSEK_df["Low"].loc[USDSEK_df["Low"].index[i], "USDSEK=X"])
highs_series = pd.Series(highs)
highs_array = np.array(highs_series)
lows_series = pd.Series(lows)
lows_array = np.array(lows_series)
closes_series = pd.Series(closes)
closes_array = np.array(closes_series)
ATR = ta.ATR(highs_array, lows_array, closes_array, timeperiod = 14)
#ATR = 0.93

#Trading
PnLs = []
positions = {}
trade_book = []

for i in range(len(USDSEK_Close_Price)):
    if i >= 50:
        if ATR[i] > 0.05:
            #print(ATR[i])
            if (sma20.loc[sma20.index[i-1], "USDSEK=X"] > sma100.loc[sma100.index[i-1], "USDSEK=X"]) and (sma20.loc[sma20.index[i], "USDSEK=X"] < sma100.loc[sma100.index[i], "USDSEK=X"]):
                # Convert USD to SEK
                USDtoSEK = risk_per_trade * USDSEK_Close_Price.loc[USDSEK_Close_Price.index[i], ticker]
                # Determine value of lots in SEK
                SEKtoLOT = one_lot * USDSEK_Close_Price.loc[USDSEK_Close_Price.index[i], ticker]
                # How many lots can we buy? 
                risk_played = USDtoSEK / SEKtoLOT
                positions[USDSEK_Close_Price.index[i]] = {
                    
                    "Order": "SELL",
                    "Price": USDSEK_Close_Price.loc[USDSEK_Close_Price.index[i], "USDSEK=X"],
                    "Order Size": risk_played,
                    "ATR": ATR[i]
                }
                
                
                
                
                
                pd.concat([pd.Series(USDSEK_Close_Price.index[i], 
                                     pd.Series(USDSEK_Close_Price.loc[USDSEK_Close_Price.index[i], 
                                                                      ticker]))], ignore_index = True)
                
                print(f"SELL @ {USDSEK_Close_Price.index[i]} {USDSEK_Close_Price.loc[USDSEK_Close_Price.index[i], ticker]}")
                print(SEKtoLOT)
                
            elif (sma20.loc[sma20.index[i-1], "USDSEK=X"] < sma100.loc[sma100.index[i-1], "USDSEK=X"]) and (sma20.loc[sma20.index[i], "USDSEK=X"] > sma100.loc[sma100.index[i], "USDSEK=X"]):
                print(f"BUY @ {USDSEK_Close_Price.index[i]} {USDSEK_Close_Price.loc[USDSEK_Close_Price.index[i], ticker]}")


# In[179]:


positions[pd.Timestamp("2021-05-12 00:00:00")]


# In[132]:


USDSEK_Close_Price.loc[USDSEK_Close_Price.index[1], "USDSEK=X"]


# In[363]:


highs_series
idk = pd.Series(2909)
highs_series

pd.concat([highs_series, idk])


# In[320]:


plt.plot(sma20)
plt.plot(sma100)


# In[254]:


#converting the list of highs to a series, and then to an array

for 

USDSEK_df['High'].loc["2020-01-14", "USDSEK=X"]

