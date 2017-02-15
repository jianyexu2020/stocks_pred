import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import relativedelta
from matplotlib.finance import candlestick_ohlc

def plot_stock(data):
    symbol = data["Symbol"][0]
    data['Date'] = data.index
    data['Date2'] = data['Date'].apply(lambda d: mdates.date2num(d.to_pydatetime()))
    tuples = [tuple(x) for x in data[['Date2', 'Open', 'High', 'Low', 'Adj_Close']].values]
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("data for stock: " + symbol)
    candlestick_ohlc(ax, tuples, width=.6, colorup='g', alpha=.4)
    ax.plot(data["Date2"], data["ema_17"])
    ax.plot(data["Date2"], data["ema_43"])
    ax2 = ax.twinx()
    ax2.set_ylabel('Volume', color='r')
    ax2.set_ylim(ymax=data["Volume"].max()*5)
    ax2.bar(data["Date2"], data["Volume"])
    xmax = data.Date2.max() + 21
    xmin = data.Date2.min() - 21
    ax2.set_xlim([xmin, xmax])
    plt.close()
    return fig
    #plt.show()

