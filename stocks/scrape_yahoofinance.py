import re
import urllib2
import calendar
import datetime
import getopt
import sys
import time
import pandas as pd

crumble_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
cookie_regex = r'set-cookie: (.*?); '
quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}'


def get_crumble_and_cookie(symbol):
    link = crumble_link.format(symbol)
    response = urllib2.urlopen(link)
    match = re.search(cookie_regex, str(response.info()))
    cookie_str = match.group(1)
    text = response.read()
    match = re.search(crumble_regex, text)
    crumble_str = match.group(1)
    return crumble_str, cookie_str


def download_quote(symbol, date_from, date_to):
    time_stamp_from = calendar.timegm(datetime.datetime.strptime(date_from, "%Y-%m-%d").timetuple())
    time_stamp_to = calendar.timegm(datetime.datetime.strptime(date_to, "%Y-%m-%d").timetuple())
    time_stamp_to += 86400
    attempts = 0
    while attempts < 5:
        crumble_str, cookie_str = get_crumble_and_cookie(symbol)
        link = quote_link.format(symbol, time_stamp_from, time_stamp_to, crumble_str)
        #print link
        r = urllib2.Request(link, headers={'Cookie': cookie_str})

        try:
            response = urllib2.urlopen(r)
            text = response.read()
            print "{} downloaded".format(symbol)
            text_list = [line.split(',') for line in text.split('\n')]
            col_names = text_list[0]
            line_values = text_list[1:]
            data_df = pd.DataFrame(data=line_values, columns=col_names)
            data_df.dropna(inplace=True)
            data_df.columns = [u'Date', u'Open', u'High', u'Low', u'Close', u'Adj_Close', u'Volume']
            data_df["Symbol"] = symbol
            data_df = data_df[['Adj_Close', 'Close', 'Date', 'High', 'Low', 'Open', 'Symbol', 'Volume']]
            return data_df
        except urllib2.URLError:
            print "{} failed at attempt # {}".format(symbol, attempts)
            attempts += 1
            time.sleep(20*attempts)
    return pd.DataFrame()

if __name__ == '__main__':
    print get_crumble_and_cookie('KO')
    from_arg = "from"
    to_arg = "to"
    symbol_arg = "symbol"
    output_arg = "o"
    opt_list = (from_arg+"=", to_arg+"=", symbol_arg+"=")
    try:
        options, args = getopt.getopt(sys.argv[1:],output_arg+":",opt_list)
    except getopt.GetoptError as err:
        print err

    for opt, value in options:
        if opt[2:] == from_arg:
            from_val = value
        elif opt[2:] == to_arg:
            to_val = value
        elif opt[2:] == symbol_arg:
            symbol_val = value
        elif opt[1:] == output_arg:
            output_val = value

    print "downloading {}".format(symbol_val)
    text = download_quote(symbol_val, from_val, to_val)

    with open(output_val, 'wb') as f:
        f.write(text)
    print "{} written to {}".format(symbol_val, output_val)