import pytz
from dateutil.relativedelta import *
from datetime import datetime
from yahoo_finance import Share
import pandas as pd
import pickle
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()

def fetch_stock_data(stock_name, start_date, end_date):
    if start_date == str(datetime.now().date()):
        print "stock %s is already up to date" % stock_name
        return
    else:
        print "updating stock: %s starting from date %s and ending on %s" % (stock_name, start_date, end_date)
        share = Share(stock_name)
        data_fecthed = pd.DataFrame(share.get_historical(start_date, end_date))
        return data_fecthed


if __name__ == "__main__":
    stocks = pickle.load(open("sp500_symbols.pk", "r"))
    off_market = ["CPGX", "GAS", "TE", "UA-C"]
    stocks = [stock for stock in stocks if stock not in off_market]

    stocks_data = pd.read_csv("stocks.csv", header=None)
    stocks_data.columns = ['Adj_Close', 'Close', 'Date', 'High', 'Low', 'Open', 'Symbol', 'Volume']
    stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)


    end_time = datetime.now() + relativedelta(days=+1)
    end_date = str(end_time.date())
    variables = ['Adj_Close', 'Close', 'Date', 'High', 'Low', 'Open', 'Symbol', 'Volume']
    stock_data_combined = pd.DataFrame(columns=variables)

    for stock_name in stocks:
        print "processing stock: %s" % stock_name
        start_date = stocks_data.ix[stocks_data.Symbol == stock_name, :].Date.max()
        start_date = str(start_date)
        print "start_date is %s and end_date is %s" % (start_date, end_date)
        stock_data = fetch_stock_data(stock_name, start_date, end_date)
        if stock_data is None:
            continue
        elif len(stock_data) == 1:
            continue
        else:
            stock_data = stock_data.sort(["Date"])
            stock_data = stock_data.reset_index(drop=True)
            print stock_data
            stock_data = stock_data
            stock_data_combined = pd.concat([stock_data_combined, stock_data])

    with open('stocks.csv', 'a+') as f:
        stock_data_combined.to_csv(f, header=False, index=False)
