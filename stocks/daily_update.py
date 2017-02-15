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
    if start_date < str(end_date):
        print "fetching stock data: %s starting from date %s and ending on %s" % (stock_name, start_date, end_date)
        share = Share(stock_name)
        data = pd.DataFrame(share.get_historical(start_date, end_date))
        return data

start_time = datetime.now()
if __name__ == "__main__":
    stocks_data = pd.read_csv("stocks.csv", header=None)
    stocks_data.columns = ['Adj_Close', 'Close', 'Date', 'High', 'Low', 'Open', 'Symbol', 'Volume']
    stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)
    stocks = list(stocks_data["Symbol"].unique())
    off_market = ["CPGX", "GAS", "TE", "UA-C"]
    stocks = [stock for stock in stocks if stock not in off_market]
    end_time = datetime.now()# + relativedelta(days=+1)
    end_date = str(end_time.date())

    #stocks = ["GILD"]
    while True:
        updated_this_round = 0
        updated_stocks = []
        variables = ['Adj_Close', 'Close', 'Date', 'High', 'Low', 'Open', 'Symbol', 'Volume']
        stock_data_combined = pd.DataFrame(columns=variables)
        for stock_name in stocks:
            #print "processing stock: %s" % stock_name
            start_date = stocks_data.ix[stocks_data.Symbol == stock_name, :].Date.max()
            start_date = datetime.strptime(str(start_date),'%Y-%m-%d') #+ relativedelta(days=+1)
            start_date = str(start_date.date())
            print "start_date is %s and end_date is %s" % (start_date, end_date)
            if start_date < end_date:
                stock_data = fetch_stock_data(stock_name, start_date, end_date)
                if stock_data.Date.max() == end_date :
                    print stock_data
                    stock_data = stock_data.sort_values(by=["Date"])
                    stock_data = stock_data.reset_index(drop=True)
                    updated_stocks.append(stock_name)
                    stock_data_combined = pd.concat([stock_data_combined, stock_data])
                    updated_this_round += 1
                else:
                    print "Failed updating most recent data for stock %s" % stock_name
                    continue
            else:
                print "skip updating because stock %s is already updated" % stock_name
                updated_stocks.append(stock_name)
        print "This round updated %d stocks" % updated_this_round
        if updated_this_round:
            with open('stocks.csv', 'a+') as f:
                stock_data_combined.to_csv(f, header=False, index=False)
            stocks = [stock for stock in stocks if stock not in updated_stocks]
        min_elapsed = (datetime.now() - start_time)/60
        if len(stocks) <= 5:
            print "Only 5 stocks not updated, stop"
            break
        if min_elapsed.total_seconds()/60.0 > 45.0:
            print "update took more than 45 min, stop"
            break

print "The stocks not updated are %s" % str(stocks)
print "data update took %s seconds" % min_elapsed