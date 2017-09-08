import pytz
from datetime import datetime
#from yahoo_finance import Share # not working since May 2017
from stocks.scrape_yahoofinance import download_quote
import pandas as pd
import time
from random import randint
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()
STOCKS_CSV = "C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\stocks\stocks.csv"
NAMES = ['Adj_Close', 'Close', 'Date', 'High', 'Low', 'Open', 'Symbol', 'Volume']

def fetch_stock_data(stock_name, start_date, end_date):
    if start_date < str(end_date):
        print "fetching stock data: %s starting from date %s and ending on %s" % (stock_name, start_date, end_date)
        data = download_quote(stock_name, start_date, end_date)
        return data


def daily_update_stocks():
    start_time = datetime.now()
    stocks_data = pd.read_csv(STOCKS_CSV, names=NAMES, header=None)
    stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)
    stocks = list(stocks_data["Symbol"].unique())
    off_market = ["SE", "CPGX", "GAS", "TE", "UA-C", "YHOO"]
    stocks = [stock for stock in stocks if stock not in off_market]
    end_time = datetime.now()
    end_date = str(end_time.date())

    #stocks = ["GILD"]
    while True:
        updated_this_round = 0
        updated_stocks = []
        stock_data_combined = pd.DataFrame(columns=NAMES)
        for stock_name in stocks:
            time.sleep(randint(1,5))
            #print "processing stock: %s" % stock_name
            start_date = stocks_data.ix[stocks_data.Symbol == stock_name, :].Date.max()
            start_date = datetime.strptime(str(start_date),'%Y-%m-%d') #+ relativedelta(days=+1)
            start_date = str(start_date.date())
            print "start_date is %s and end_date is %s" % (start_date, end_date)
            if start_date < end_date:
                stock_data = fetch_stock_data(stock_name, start_date, end_date)
                times = 1
                while len(stock_data) == 0 and times < 2:
                    time.sleep(10)
                    stock_data = fetch_stock_data(stock_name, start_date, end_date)
                    times += 1
                if len(stock_data) == 0:
                    print "Failed updating most recent data for stock %s" % stock_name
                    continue
                else:
                    print stock_data
                    stock_data = stock_data.sort_values(by=["Date"])
                    stock_data = stock_data.reset_index(drop=True)
                    stock_data_combined = pd.concat([stock_data_combined, stock_data])
                    updated_this_round += 1
            else:
                print "skip updating because stock %s is already updated" % stock_name
            updated_stocks.append(stock_name)
            if updated_this_round == 5:
                with open(STOCKS_CSV, 'a+') as f:
                    stock_data_combined.to_csv(f, header=False, index=False)
                print "This round updated %d stocks" % updated_this_round
                break
        stocks = [stock for stock in stocks if stock not in updated_stocks]
        min_elapsed = (datetime.now() - start_time)/60
        if len(stocks) <= 5:
            print "Only 5 stocks not updated, stop"
            break

    print "The stocks not updated are %s" % str(stocks)
    print "data update took %s seconds" % min_elapsed

    # drop duplicates and save the data to csv
    stocks_data = pd.read_csv(STOCKS_CSV, names=NAMES, header=None)
    stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)
    with open(STOCKS_CSV, 'wb') as f:
        stocks_data.to_csv(f, header=False, index=False)

    return stocks_data

if __name__ == "__main__":
    daily_update_stocks()