import pandas as pd
import numpy as np
import talib

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

def add_features(stock):
    stock.loc[:, "stock_index"] = stock[["Symbol", "Date"]].apply(lambda x: '_'.join(x), axis=1)
    stock.loc[:, "Date"] = stock["Date"].apply(lambda x: pd.to_datetime(x, format="%Y-%m-%d"))
    stock = stock.set_index(['stock_index'])
    stock = stock.sort_index()
    print stock.iloc[-3:, :]

    stock["Adj_Close"] = stock["Adj_Close"].astype(float)
    stock["Volume"] = stock["Volume"].astype(float)
    stock["Adj_Close_Volume"] = stock["Adj_Close"] * stock["Volume"]
    stock["High"] = stock["High"].astype(float)
    stock["Low"] = stock["Low"].astype(float)

    close = np.array(stock.Adj_Close)
    volume = np.array(stock.Volume)
    high = np.array(stock.High)
    low = np.array(stock.Low)

    stock.loc[:, "macd1"], stock.loc[:, "macd2"], stock.loc[:, "macd"] = talib.MACD(close,
                                                                                    fastperiod=12,
                                                                                    slowperiod=26,
                                                                                    signalperiod=9)

    stock.loc[:, "rsi"] = talib.RSI(close, 12)

    for i in xrange(10, 60, 10):
        ema_var_name = "ema_" + str(i)
        v_ema_var_name = "v_ema_" + str(i)
        stock.loc[:, ema_var_name] = talib.EMA(close, i)
        stock.loc[:, v_ema_var_name] = talib.EMA(volume, i)

    for i in xrange(100, 200, 100):
        ema_var_name = "ema_" + str(i)
        v_ema_var_name = "v_ema_" + str(i)
        stock.loc[:, ema_var_name] = talib.EMA(close, i)
        stock.loc[:, v_ema_var_name] = talib.EMA(volume, i)

    stock.loc[:, "slowk"], stock.loc[:, "slowd"] = talib.STOCH(high=high,
                                                               low=low,
                                                               close=close,
                                                               fastk_period=14,
                                                               slowk_period=3,
                                                               slowk_matype=0,
                                                               slowd_period=3,
                                                               slowd_matype=0)

    stock.loc[:,"rolling_min_7d"] = pd.rolling_min(stock["Adj_Close"], window=7)
    stock.loc[:, "rolling_max_7d"] = pd.rolling_max(stock["Adj_Close"], window=7)
    stock.loc[:, "rolling_std_7d"] = pd.rolling_std(stock["Adj_Close"], window=7)
    stock.loc[:, "rolling_skew_7d"] = pd.rolling_skew(stock["Adj_Close"], window=7)
    stock.loc[:,"rolling_min_1m"] = pd.rolling_min(stock["Adj_Close"], window=30)
    stock.loc[:, "rolling_max_1m"] = pd.rolling_max(stock["Adj_Close"], window=30)
    stock.loc[:, "rolling_std_1m"] = pd.rolling_std(stock["Adj_Close"], window=30)
    stock.loc[:, "rolling_skew_1m"] = pd.rolling_skew(stock["Adj_Close"], window=30)
    stock.loc[:,"rolling_min_1y"] = pd.rolling_min(stock["Adj_Close"], window=252)
    stock.loc[:, "rolling_max_1y"] = pd.rolling_max(stock["Adj_Close"], window=252)
    stock.loc[:, "rolling_std_1y"] = pd.rolling_std(stock["Adj_Close"], window=252)
    stock.loc[:, "rolling_skew_1y"] = pd.rolling_skew(stock["Adj_Close"], window=252)
    stock.loc[:, "cv_rolling_min_7d"] = pd.rolling_min(stock["Adj_Close_Volume"], window=7)
    stock.loc[:, "cv_rolling_max_7d"] = pd.rolling_max(stock["Adj_Close_Volume"], window=7)
    stock.loc[:, "cv_rolling_std_7d"] = pd.rolling_std(stock["Adj_Close_Volume"], window=7)
    stock.loc[:, "cv_rolling_skew_7d"] = pd.rolling_skew(stock["Adj_Close_Volume"], window=7)
    stock.loc[:, "cv_rolling_min_1m"] = pd.rolling_min(stock["Adj_Close_Volume"], window=30)
    stock.loc[:, "cv_rolling_max_1m"] = pd.rolling_max(stock["Adj_Close_Volume"], window=30)
    stock.loc[:, "cv_rolling_std_1m"] = pd.rolling_std(stock["Adj_Close_Volume"], window=30)
    stock.loc[:, "cv_rolling_skew_1m"] = pd.rolling_skew(stock["Adj_Close_Volume"], window=30)
    stock.loc[:, "cv_rolling_min_1y"] = pd.rolling_min(stock["Adj_Close_Volume"], window=252)
    stock.loc[:, "cv_rolling_max_1y"] = pd.rolling_max(stock["Adj_Close_Volume"], window=252)
    stock.loc[:, "cv_rolling_std_1y"] = pd.rolling_std(stock["Adj_Close_Volume"], window=252)
    stock.loc[:, "cv_rolling_skew_1y"] = pd.rolling_skew(stock["Adj_Close_Volume"], window=252)

    #Shift the historical data to today
    variables = [x for x in stock.columns if x not in ["Date", "Symbol"]]
    lag_data_1 = buildLaggedFeatures(stock[variables], lag=1, dropna=False)
    lag_data_7 = buildLaggedFeatures(stock[variables], lag=7, dropna=False)
    lag_data_15 = buildLaggedFeatures(stock[variables], lag=15, dropna=False)
    lag_data_30 = buildLaggedFeatures(stock[variables], lag=30, dropna=False)
    lag_data_60 = buildLaggedFeatures(stock[variables], lag=60, dropna=False)
    stock_with_lag_data = pd.merge(stock, lag_data_1, left_index=True, right_index=True)
    stock_with_lag_data = pd.merge(stock_with_lag_data, lag_data_7, left_index=True, right_index=True)
    stock_with_lag_data = pd.merge(stock_with_lag_data, lag_data_15, left_index=True, right_index=True)
    stock_with_lag_data = pd.merge(stock_with_lag_data, lag_data_30, left_index=True, right_index=True)
    stock_with_lag_data = pd.merge(stock_with_lag_data, lag_data_60, left_index=True, right_index=True)



    stock_with_lag_data.dropna(inplace=True)
    stock_with_lag_data["increase_from_last_day"] \
        = (stock_with_lag_data["Adj_Close"] - stock_with_lag_data["Adj_Close_lag1"]) / stock_with_lag_data[
        "Adj_Close_lag1"] * 100
    stock_with_lag_data["increase_from_last_week"] \
        = (stock_with_lag_data["Adj_Close"] - stock_with_lag_data["Adj_Close_lag7"]) / stock_with_lag_data[
        "Adj_Close_lag7"] * 100
    return stock_with_lag_data