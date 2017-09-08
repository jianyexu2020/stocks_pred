#!/usr/bin/python
import pandas as pd
import numpy as np
from stocks.feature_builder import add_features

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

STOCKS_CSV = "C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\stocks\stocks.csv"


def build_features():
    stocks_data = pd.read_csv(STOCKS_CSV, na_values=["null"])
    stocks_data.columns = ['Adj_Close','Close','Date','High','Low','Open','Symbol','Volume']
    stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)
    stocks_data.dropna(axis=0, how="any", inplace=True)
    stocks_data[['Adj_Close','Close','High','Low','Open']] \
        = stocks_data[['Adj_Close','Close','High','Low','Open']].apply(lambda x: x.astype(float))
    stock_names = list(stocks_data["Symbol"].unique())
    report_today = pd.DataFrame()
    stocks_with_lag_data = pd.DataFrame()
    #stock_names = ["AAPL", "GILD"]
    for stock_name in stock_names:
        print "Processing stock: %s" % stock_name
        stock = stocks_data.loc[(stocks_data.Symbol == stock_name),:]
        if stock.shape[0] <= 100:
            continue
        stock_with_lag_data = add_features(stock)
        stocks_with_lag_data = stocks_with_lag_data.append(stock_with_lag_data)

    report_today_cols = [ "Adj_Close", "Close","High","Low","Open","Volume", "macd", "rsi", "slowk", "slowd",
                          "ema_10", "v_ema_10"]
    max_date = stocks_with_lag_data.Date.max()
    report_today = stocks_with_lag_data.loc[stocks_with_lag_data.Date==max_date, report_today_cols]
    for var in report_today_cols:
        report_today[var] = report_today[var].astype("float")

    report_today["close_over_ema_10"] = report_today["Adj_Close"] / report_today["ema_10"]
    report_today["volume_over_ema_10"] = report_today["Volume"] / report_today["v_ema_10"]

    report_today = np.round(report_today, 2)
    report_today.sort_values(by=["rsi"], ascending=True, inplace=True)

    print report_today

    report_today.to_csv("report_today.csv", sep='\t')
    stocks_with_lag_data.to_csv("stocks_with_lag_data.csv", sep='\t')
    return report_today

if __name__ == "__main__":
    build_features()