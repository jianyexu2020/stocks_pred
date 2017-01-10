#!/usr/bin/env python
import urllib
import pytz
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
from pandas.io.data import DataReader
import pickle
from yahoo_finance import Share
import pandas as pd


SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()

#scrape the list of SPY
def scrape_list(site):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.Request(site, headers=hdr)
    page = urllib.urlopen(req)
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


if __name__ == "__main__":
    start_date = '2012-08-31'
    end_date = str(datetime.now().date())
    sector_tickers = scrape_list(SITE)
    stocks = [sybl for key, value in sector_tickers.items() for sybl in value]
    print(stocks)
    #print len(stocks)
    with open("sp500_symbols.pk",'w') as f:
        pickle.dump(stocks, f)
    
    stocks = stocks + ["QQQ", "SPY", "GLD", "SLV", "HAWK", 
                       "TSLA", "BABA", "CELG", "NFLX", "TWTR"]
    #stocks = ["AAPL"]
    
    columns = ['Adj_Close','Close','Date','High','Low','Open','Symbol','Volume']
    stocks_data = pd.DataFrame(columns=columns)

    for stock in stocks:
        share = Share(stock)
        print("Fetching data for stock %s" % stock)
        stock_data = pd.DataFrame(share.get_historical(start_date, end_date))
        #print stock_data
    
        with open('stocks.csv', 'a') as f:
            stock_data.to_csv(f, index=False, header=False)
