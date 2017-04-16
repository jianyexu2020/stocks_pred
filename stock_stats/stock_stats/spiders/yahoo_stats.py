import sys
import scrapy
from selenium import webdriver
import re
from datetime import datetime
sys.path.append('C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred')
from lib.constants import SYMBOLS

#SYMBOLS = ["HAWK", "SQ"]
TODAY = str(datetime.now().date())

def hasNum(string):
    return bool(re.search(r'\d', string))


def hasComma(string):
    return bool(re.search(r',', string))


def reg_processing(string):
    string1 = re.sub(r'[\(\)\\%/&]', "", string)
    var_list1 = string1.split("\n")
    var_list2 = [re.sub(r'(.*) \d (.*)', r'\1\t\2', x) for x in var_list1]
    var_list3 = [re.sub(r'([a-zA-Z]) +([a-zA-Z])', r'\1_\2', x) for x in var_list2]
    var_list4 = [re.sub(r'([a-zA-Z]) \d+ ([a-zA-Z])', r'\1_\2', x) for x in var_list3]
    var_list5 = [x.strip() for x in var_list4 if hasNum(x)]
    var_list6 = [x for x in var_list5 if not hasComma(x)]
    var_list7 = [re.sub(r'([\d+]) ', r'\1_', x)for x in var_list6]
    var_list8 = [re.sub(r' ', r'\t', x) for x in var_list7]
    var_dict = dict([(x.split('\t')[0], x.split('\t')[1]) for x in var_list8])
    return var_dict


class YahooStats(scrapy.Spider):
    name = "yahoo_stats"

    def __init__(self):
        self.driver = webdriver.Chrome("C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\chromedriver_win32\chromedriver.exe")

    def start_requests(self):
        domain = "https://finance.yahoo.com/quote/"
        end_of_url = "/key-statistics"
        for symbol in SYMBOLS:
            url = domain + symbol + end_of_url
            print "processing url %s" % url
            data = scrapy.Request(url=url, callback=self.parse)
            yield data

    def parse(self, response):
        self.driver.get(response.url)
        stats_obj = self.driver.find_element_by_xpath("//*[@id='main-0-Quote-Proxy']/section/div[2]/section/div")
        raw_text = stats_obj.text
        symbol = re.findall(r'[A-Z]+', response.url)[0]
        data_dict = reg_processing(raw_text)
        data_dict["symbol"] = symbol
        data_dict["date"] = TODAY
        return data_dict
