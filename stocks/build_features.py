#!/usr/bin/python

import pandas as pd
import numpy as np
import talib
import pickle
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

STOCKS_CSV = "C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\stocks\stocks.csv"

def buildLaggedFeatures(s,lag=2,dropna=True):
    """
    Builds a new DataFrame to facilitate regressing over all possible lagged features
    """
    if type(s) is pd.DataFrame:
        new_dict={}
        for col_name in s:
            new_dict[col_name]=s[col_name]
            # create lagged Series
            #for l in range(1,lag+1):
            new_dict['%s_lag%d' %(col_name,lag)]=s[col_name].shift(lag)
        lag_dict = {key: value for key, value in new_dict.items() if "lag" in key}
        res=pd.DataFrame(lag_dict,index=s.index)

    elif type(s) is pd.Series:
        the_range=range(lag+1)
        #res=pd.concat([s.shift(i) for i in the_range],axis=1)
        #res.columns=['lag_%d' %i for i in the_range]
        res = pd.concat([s.shift(lag)], axis=1)
        res.columns = ['lag_%d' % lag]
    else:
        print 'Only works for DataFrame or Series'
        return None
    if dropna:
        return res.dropna()
    else:
        return res


if __name__ == "__main__":
    try:
        myfile = open("report_today.csv", "a+")
    except IOError:
        print "Could not open file! Please close csv file!"
    # read stocks data from csv file
    stocks_data = pd.read_csv(STOCKS_CSV)
    stocks_data.columns = ['Adj_Close','Close','Date','High','Low','Open','Symbol','Volume']
    stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)
    stock_names = list(stocks_data["Symbol"].unique())
    report_today = pd.DataFrame()
    stocks_with_lag_data = pd.DataFrame()

    #stock_names = ["AAPL"]
    for stock_name in stock_names:
        print "Processing stock: %s" % stock_name
        stock =  stocks_data.loc[(stocks_data.Symbol == stock_name),:]
        if stock.shape[0] <= 100:
            continue
        stock.loc[:,"Adj_Close"] = stock.loc[:,"Adj_Close"].astype(float)
        stock.loc[:,"Volume"] = stock.loc[:,"Volume"].astype(float)
        #stock.loc[:,"Date"] = pd.to_datetime(stock.loc[:,"Date"])
        stock.loc[:,"stock_index"] = stock[["Symbol", "Date"]].apply(lambda x: '_'.join(x), axis=1)
        stock = stock.set_index(['stock_index'])
        stock = stock.sort_index()
        print stock.iloc[-3:,:]

        close = np.array(stock.Adj_Close)
        volume = np.array(stock.Volume)
        high = np.array(stock.High)
        low = np.array(stock.Low)
        close_noadj = np.array(stock.Close)

        stock.loc[:,"macd1"], stock.loc[:,"macd2"], stock.loc[:,"macd"] = \
            talib.MACD(close,
                       fastperiod=12,
                       slowperiod=26,
                       signalperiod=9)
        
        stock.loc[:, "rsi"] = talib.RSI(close, 12)

        for i in xrange(10, 60, 10):
            ema_var_name = "ema_" + str(i)
            v_ema_var_name = "v_ema_" + str(i)
            stock.loc[:,ema_var_name] = talib.EMA(close, i)
            stock.loc[:,v_ema_var_name] = talib.EMA(volume, i)

        for i in xrange(100, 200, 100):
            ema_var_name = "ema_" + str(i)
            v_ema_var_name = "v_ema_" + str(i)
            stock.loc[:,ema_var_name] = talib.EMA(close, i)
            stock.loc[:,v_ema_var_name] = talib.EMA(volume, i)

        stock.loc[:,"slowk"], stock.loc[:, "slowd"] = talib.STOCH(high=high,
                                                                  low=low,
                                                                  close=close_noadj,
                                                                  fastk_period=14,
                                                                  slowk_period=3, 
                                                                  slowk_matype=0,
                                                                  slowd_period=3, 
                                                                  slowd_matype=0)

        report_today = report_today.append(stock.iloc[-1,:])
        lag_data_1 = buildLaggedFeatures(stock, lag=1, dropna=False)
        lag_data_30 = buildLaggedFeatures(stock, lag=30, dropna=False)
        lag_data_60 = buildLaggedFeatures(stock, lag=60, dropna=False)
        stock_with_lag_data = pd.merge(stock, lag_data_1, left_index=True, right_index=True)
        stock_with_lag_data = pd.merge(stock_with_lag_data, lag_data_30, left_index=True, right_index=True)
        stock_with_lag_data = pd.merge(stock_with_lag_data, lag_data_60, left_index=True, right_index=True)
        stock_with_lag_data.dropna(inplace=True)
        stock_with_lag_data["increase_from_last_day"] \
            = (stock_with_lag_data["Adj_Close"] -  stock_with_lag_data["Adj_Close_lag1"]) / stock_with_lag_data["Adj_Close_lag1"] * 100
        stock_with_lag_data["target"] = stock_with_lag_data["increase_from_last_day"].apply(lambda x: 1 if x > 0 else 0)
        #print stock_with_lag_data.tail()
        stocks_with_lag_data = stocks_with_lag_data.append(stock_with_lag_data)

    report_today_cols = [ "Adj_Close", "Close","High","Low","Open",
                          "Volume", "macd", "rsi", "slowk", "slowd",
                          "ema_10", "v_ema_10"]

    report_today = report_today[report_today_cols]
    for var in report_today_cols:
        report_today[var] = report_today[var].astype("float")

    report_today["close_over_ema_10"] = report_today["Adj_Close"] / report_today["ema_10"]
    report_today["volume_over_ema_10"] = report_today["Volume"] / report_today["v_ema_10"]

    report_today = np.round(report_today, 2)
    report_today.sort_values(by=["rsi"], ascending=True, inplace=True)

    print report_today

    report_today.to_csv("report_today.csv", sep='\t')
    stocks_with_lag_data.to_csv("stocks_with_lag_data.csv", sep='\t')
