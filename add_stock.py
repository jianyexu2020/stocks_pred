#add stocks to the stocks_csv file
from dateutil.relativedelta import *
from datetime import datetime
from yahoo_finance import Share
import pandas as pd
from daily_update import fetch_stock_data

start_date = '2012-08-31'
end_date = str(datetime.now().date())


def add_stock(symbol, start_time, end_time):
    stock_data = fetch_stock_data(symbol, start_time, end_time)
    with open('stocks.csv', 'a+') as f:
        stock_data.to_csv(f, header=False, index=False)

if __name__ == "__main__":
    add_stock("UVXY", start_date, end_date)
