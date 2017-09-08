import numpy as np
import pandas as pd
import talib
from matplotlib.backends.backend_pdf import PdfPages

from lib.make_plot import plot_stock
STOCKS_CSV = "C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\stocks\stocks.csv"


def split_adjust(stock_data):
    stock_data.loc[:,"Split_ratio"] = stock_data.loc[:,"Close"] / stock_data.loc[:,"Adj_Close"]
    stock_data.loc[:,"Open"] = stock_data.loc[:,"Open"] / stock_data.loc[:,"Split_ratio"]
    stock_data.loc[:,"High"] = stock_data.loc[:,"High"] / stock_data.loc[:,"Split_ratio"]
    stock_data.loc[:,"Low"] = stock_data.loc[:,"Low"] / stock_data.loc[:,"Split_ratio"]
    return stock_data


daily_data = pd.read_csv(STOCKS_CSV, header=None)
daily_data.columns = ['Adj_Close','Close','Date','High','Low','Open','Symbol','Volume']
daily_data["Date"] = pd.to_datetime(daily_data["Date"])
daily_data.set_index("Date", inplace=True)

stocks = list(daily_data.Symbol.unique())

stocks = sorted(stocks)
print stocks
ohlc_dict = {'Open':'first','High':'max','Low':'min','Close': 'last','Volume': 'sum','Adj_Close': 'last', 'Symbol':'max'}
weekly_data = pd.DataFrame(columns=['Adj_Close','Close','Date','High','Low','Open','Symbol','Volume'])

#stocks = ["AAPL", "GILD", "M"]
with PdfPages('weekly_data_plot.pdf') as pdf:
    for stock in stocks:
        stock_daily_data = daily_data.loc[daily_data.Symbol==stock, :]
        stock_daily_data = split_adjust(stock_daily_data)
        stock_weekly_data = stock_daily_data.resample('W', how=ohlc_dict, closed='right', label='right')
        moving_averages = [17, 43]
        close = np.array(stock_weekly_data["Adj_Close"].astype("float"))
        volume = np.array(stock_weekly_data["Volume"].astype("float"))
        for i in moving_averages:
            ema_var_name = "ema_" + str(i)
            v_ema_var_name = "v_ema_" + str(i)
            stock_weekly_data.loc[:, ema_var_name] = talib.EMA(close, i)
            stock_weekly_data.loc[:, v_ema_var_name] = talib.EMA(volume, i)
        stock_weekly_data.dropna()
        fig = plot_stock(stock_weekly_data)
        print "Saving stock %s" % stock
        pdf.savefig(fig)
        weekly_data= pd.concat([weekly_data, stock_weekly_data])

weekly_data.to_csv("weekly_data.csv")