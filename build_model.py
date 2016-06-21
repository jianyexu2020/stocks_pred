import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation


#read data and split data
stocks_with_lag_data = pd.read_csv("stocks_with_lag_data.csv", sep='\t')
column_names = stocks_with_lag_data.columns.tolist()
column_names[0] = "stocks_index"
stocks_with_lag_data.columns = column_names
stocks_with_lag_data = stocks_with_lag_data.set_index("stocks_index")
print stocks_with_lag_data.head()

predictors = [x for x in column_names if "lag" in x and "Date" not in x ]

#standardized data
for predictor in predictors:
    if "v_" in predictor:
        stocks_with_lag_data[predictor] =   stocks_with_lag_data["Volume"] / stocks_with_lag_data[predictor]
    elif "ema_" in predictor:
        stocks_with_lag_data[predictor] =   stocks_with_lag_data["Adj_Close"] / stocks_with_lag_data[predictor]
    elif "High" in predictor or "Low" in predictor or "Open" in predictor:
        stocks_with_lag_data[predictor] =   stocks_with_lag_data["Adj_Close"] / stocks_with_lag_data[predictor]


X = stocks_with_lag_data[predictors]
y = stocks_with_lag_data["target"]

print X.tail()
print y.tail()


