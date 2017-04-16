import sqlalchemy
import pandas as pd
from pandas.io import sql
import json

save_to_mysql = """
LOAD DATA LOCAL INFILE
'C:/Users/ralph/OneDrive/Documents/GitHub/stocks_pred/stocks/stocks.csv'
IGNORE INTO TABLE stocks
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
"""

create_stocks_table = """
create table stocks (
Adj_Close float,
Close  float,
Date  date,
High  float,
Low  float,
Open float,
Symbol Varchar(255),
Volume  bigint
)
"""



def save_data_to_mysql():
    engine = sqlalchemy.create_engine('mysql://root:Shaohui805@localhost')
    engine.execute("use stocks;")
    engine.execute(save_to_mysql)

if _name__ == "__main__":
    save_data_to_mysql()
    with open("C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\stock_stats\\test.json") as f:
        stock_stats_json = json.load(f)
    stock_stats = pd.DataFrame(stock_stats_json)
    stock_stats.to_csv("stock_stats.csv", header=True, index=False)




#delete from stocks;

# engine = sqlalchemy.create_engine('mysql://root:Shaohui805@localhost')
# engine.execute("use stocks;")
# df = pd.read_sql( "select * from stocks;", engine)
# df.to_csv("stocks.csv", index=False, header=False)
#

