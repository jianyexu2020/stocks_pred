#!/usr/bin/env python
import urllib2
import pytz
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime
from pandas.io.data import DataReader
import pickle


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


sector_tickers = scrape_list(SITE)


# section 2
from yahoo_finance import Share
import pandas as pd

#start and end date
start_date = '2013-01-01'
end_date =  str(datetime.today())[:10]

stocks = [sybl for key, value in sector_tickers.items() for sybl in value]
with open("sp500_symbols.pk",'w') as f:
    pickle.dump(stocks, f)


columns = ['Adj_Close','Close','Date','High','Low','Open','Symbol','Volume']
stocks_data = pd.DataFrame(columns=columns)

for stock in stocks:
    #print stock
    share = Share(stock)
    stock_data = pd.DataFrame(share.get_historical('2013-01-01', '2016-06-20'))
    stocks_data = stocks_data.append(stock_data,ignore_index=True)

stocks_data.to_csv("stocks.csv", index=False)
