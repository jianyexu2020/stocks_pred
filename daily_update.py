#!/usr/bin/env python
import urllib2
import pytz
import pandas as pd
from dateutil.relativedelta import *

from bs4 import BeautifulSoup
from datetime import datetime
from pandas.io.data import DataReader

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

#scrape the list of SPY
def scrape_list(site):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)

    table = soup.find('table', {'class': 'wikitable sortable'})
    sector_tickers = dict()
    for row in table.findAll('tr'):
        col = row.findAll('td')
        if len(col) > 0:
            sector = str(col[3].string.strip()).lower().replace(' ', '_')
            ticker = str(col[0].string.strip())
            if sector not in sector_tickers:
                sector_tickers[sector] = list()
            sector_tickers[sector].append(ticker)
    return sector_tickers



def fetch_stock_data(stock_name, start_date, end_date):
    if start_date == str(datetime.now().date()):
        print "stock %s is already up to date" % stock_name
    else:
        print "updating stock: %s starting from date %s and ending on %s" % (stock_name, start_date, end_date)
        share = Share(stock)
        stock_data = pd.DataFrame(share.get_historical(start_date, end_date))


if __name__ == "__main__":
    sector_tickers = scrape_list(SITE)
    sector_tickers = pickle.load(open("sp500_symbols.pk","r"))
    off_market = ["CPGX", "GAS", "TE", "UA-C"]
    sector_tickers = [stock for stock in sector_tickers if stock not in off_market]

    # section 2
    stocks_data = pd.read_csv("stocks.csv")
    stocks_data.drop_duplicates(["Date", "Symbol"], inplace=True)

    #stocks = [sybl for key, value in sector_tickers.items() for sybl in value ]
    stocks = sector_tickers
    #stocks = ["DIS", "WMT"]
    columns = ['Adj_Close','Close','Date','High','Low','Open','Symbol','Volume']

    end_time =  datetime.now() + relativedelta(days=+1)
    end_date = str(end_time.date())

    for stock_name in stocks:
        start_date = stocks_data.ix[stocks_data.Symbol==stock,:].Date.max()
        start_date = str(start_date)
        stock_data = fetch_stock_data(stock_name, start_date, end_date)
        print stock_data
        if stock_data is None:
            continue
        elif len(stock_data) == 1:
            continue
        else:
            stock_data = stock_data.sort(["Date"])
            stock_data = stock_data.reset_index(drop=True)
            print stock_data
            stock_data = stock_data.iloc[1:,:]
            print stock_data
            with open('stocks.csv', 'a') as f:
                stock_data.to_csv(f, header=False, index=False)
