#!/usr/bin/python

import pandas as pd
import numpy as np
import talib
import pickle
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def buildLaggedFeatures(s,lag=2,dropna=True):
    """
    Builds a new DataFrame to facilitate regressing over all possible lagged features
    """
    if type(s) is pd.DataFrame:
        new_dict={}
        for col_name in s:
            new_dict[col_name]=s[col_name]
            # create lagged Series
            for l in range(1,lag+1):
                new_dict['%s_lag%d' %(col_name,l)]=s[col_name].shift(l)
        lag_dict = {key: value for key, value in new_dict.items() if "lag" in key}
        res=pd.DataFrame(lag_dict,index=s.index)

    elif type(s) is pd.Series:
        the_range=range(lag+1)
        res=pd.concat([s.shift(i) for i in the_range],axis=1)
        res.columns=['lag_%d' %i for i in the_range]
    else:
        print 'Only works for DataFrame or Series'
        return None
    if dropna:
        return res.dropna()
    else:
        return res 

stocks_data = pd.read_csv("stocks.csv")
stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)
#print stocks_data.head()

#tech_stocks = ['ACN', 'ATVI', 'ADBE', 'AKAM', 'ADS', 'GOOGL', 'GOOG', 'ADI', 'AAPL', 'AMAT', 'ADSK', 'ADP', 'AVGO', 'CA', 'CSCO', 'CTXS', 'CTSH', 'CSRA', 'EBAY', 'EA', 'EMC', 'EQIX', 'FFIV', 'FB', 'FIS', 'FSLR', 'FISV', 'GPN', 'HRS', 'HPE', 'HPQ', 'INTC', 'IBM', 'INTU', 'JNPR', 'KLAC', 'LRCX', 'LLTC', 'MA', 'MCHP', 'MU', 'MSFT', 'MSI', 'NTAP', 'NFLX', 'NVDA', 'ORCL', 'PAYX', 'PYPL', 'QRVO', 'QCOM', 'RHT', 'CRM', 'STX', 'SWKS', 'SYMC', 'TEL', 'TDC', 'TXN', 'TSS', 'VRSN', 'V', 'WDC', 'WU', 'XRX', 'XLNX', 'YHOO']
#tech_stocks = ['AAPL']
#stocks = ["AAPL"]
stocks = pickle.load(open("sp500_symbols.pk","r"))


columns = ['Adj_Close','Close','High','Low','Open','Symbol','Volume', "macd", "rsi", 
        "slowk", "slowd",
        "ema_10", "ema_20", "ema_30", "ema_40", "ema_50",
        "v_ema_10", "v_ema_20", "v_ema_30", "v_ema_40", "v_ema_50"]

latest_daily_report = pd.DataFrame(columns=columns)
stocks_with_lag_data = pd.DataFrame()
#latest_daily_report["Date"] = pd.to_datetime(latest_daily_report["Date"], format="%Y-%m-%d")

for stock in stocks:
    print "Processing stock: %s" % stock
    sybl =  stocks_data.loc[(stocks_data.Symbol == stock),:]
    if sybl.shape[0] <= 100:
        continue
    sybl.loc[:,"Adj_Close"] = sybl.loc[:,"Adj_Close"].astype(float)
    sybl.loc[:,"Volume"] = sybl.loc[:,"Volume"].astype(float)
    #sybl.loc[:,"Date"] = pd.to_datetime(sybl.loc[:,"Date"])
    sybl.loc[:,"stock_index"] = sybl[["Symbol", "Date"]].apply(lambda x: '_'.join(x), axis=1)
    sybl = sybl.set_index(['stock_index'])
    sybl = sybl.sort_index()

    close = np.array(sybl.Adj_Close)
    volumn = np.array(sybl.Volume)
    high = np.array(sybl.High)
    low = np.array(sybl.Low)
    close_noadj = np.array(sybl.Close)
    #print volumn
    macd, signal, hist = talib.MACD(np.array(close),
                                fastperiod=12,
                                slowperiod=26,
                                signalperiod=9)
    rsi = talib.RSI(np.array(close), 12)

    ema_10 = talib.EMA(np.array(close), 10)
    ema_20 = talib.EMA(np.array(close), 20)
    ema_30 = talib.EMA(np.array(close), 30)
    ema_40 = talib.EMA(np.array(close), 40)
    ema_50 = talib.EMA(np.array(close), 50)

    v_ema_10 = talib.EMA(np.array(volumn, dtype=float), 10)
    v_ema_20 = talib.EMA(np.array(volumn, dtype=float), 20)
    v_ema_30 = talib.EMA(np.array(volumn, dtype=float), 30)
    v_ema_40 = talib.EMA(np.array(volumn, dtype=float), 40)
    v_ema_50 = talib.EMA(np.array(volumn, dtype=float), 50)

    slowk, slowd = talib.STOCH(high=high, low=low, close=close_noadj ,fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    #print slowk.shape
    #print slowd.shape
    #print rsi.shape


    sybl.loc[:,"macd"] = hist
    sybl.loc[:,"rsi"] = rsi
    sybl.loc[:,"slowk"] = slowk
    sybl.loc[:,"slowd"] = slowd

    sybl.loc[:,"ema_10"] = ema_10
    sybl.loc[:,"ema_20"] = ema_20
    sybl.loc[:,"ema_30"] = ema_30
    sybl.loc[:,"ema_40"] = ema_40
    sybl.loc[:,"ema_50"] = ema_50

    sybl.loc[:,"v_ema_10"] = v_ema_10
    sybl.loc[:,"v_ema_20"] = v_ema_20
    sybl.loc[:,"v_ema_30"] = v_ema_30
    sybl.loc[:,"v_ema_40"] = v_ema_40
    sybl.loc[:,"v_ema_50"] = v_ema_50


    #if sybl["rsi"][len(sybl.index)-1] < 30 \
    #or sybl["rsi"][len(sybl.index)-1] > 70:
    #print sybl.iloc[-2:,:]
    latest_daily_report = latest_daily_report.append(sybl.iloc[-1,:])#ignore_index=True)#.drop("index", axis=1)
    if latest_daily_report.shape[0] > 500:
        break
    lag_data = buildLaggedFeatures(sybl, lag=1, dropna=False)
    sybl_with_lag_data = pd.merge(sybl, lag_data, left_index=True, right_index=True)
    sybl_with_lag_data.dropna(inplace=True) 
    sybl_with_lag_data["increase_from_last_day"] = (sybl_with_lag_data["Adj_Close"] -  sybl_with_lag_data["Adj_Close_lag1"]) / sybl_with_lag_data["Adj_Close_lag1"] * 100
    sybl_with_lag_data["target"] = sybl_with_lag_data["increase_from_last_day"].apply(lambda x: 1 if x > 0 else 0)
    #print sybl_with_lag_data
    stocks_with_lag_data = stocks_with_lag_data.append(sybl_with_lag_data) 

latest_daily_report = latest_daily_report.iloc[:,:11]
del latest_daily_report["Symbol"]
latest_daily_report["Adj_Close"] = latest_daily_report["Adj_Close"].astype("float")
latest_daily_report["Close"] = latest_daily_report["Close"].astype("float")
latest_daily_report["Open"] = latest_daily_report["Open"].astype("float")
latest_daily_report["High"] = latest_daily_report["High"].astype("float")
latest_daily_report["Low"] = latest_daily_report["Low"].astype("float")
latest_daily_report["Volume"] = latest_daily_report["Volume"].astype("float")
latest_daily_report["rsi"] = latest_daily_report["rsi"].astype("float")
latest_daily_report["macd"] = latest_daily_report["macd"].astype("float")
latest_daily_report["slowk"] = latest_daily_report["slowk"].astype("float")
latest_daily_report["slowd"] = latest_daily_report["slowd"].astype("float")


latest_daily_report = np.round(latest_daily_report, 2)
latest_daily_report.sort(["rsi"], ascending=True, inplace=True)

latest_daily_report.to_csv("latest_daily_report.csv", sep='\t')
stocks_with_lag_data.to_csv("stocks_with_lag_data.csv", sep='\t')
