#!/usr/bin/python

import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn import metrics
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 30)

predictors_need_norm = [
 'Close_lag1',
 'High_lag1',
 'Low_lag1',
 'Open_lag1',
 'ema_10_lag1',
 'ema_20_lag1',
 'ema_30_lag1',
 'ema_40_lag1',
 'ema_50_lag1',
 'v_ema_10_lag1',
 'v_ema_20_lag1',
 'v_ema_30_lag1',
 'v_ema_40_lag1',
 'v_ema_50_lag1']


def normalize_lag(df, lag_col):
    if "v_" in lag_col: 
        df[lag_col] = df[lag_col] / df['Volume_lag1']
    else:
        df[lag_col] = df[lag_col] / df['Adj_Close_lag1']


data = pd.read_csv("stocks_with_lag_data.csv", sep='\t')
data["target"] = data["increase_from_last_day"].apply(lambda x: 1 if x > 1 else 0)
predictors = [x for x in data.columns if "lag1" in x]
predictors.remove("Symbol_lag1")
predictors.remove("Date_lag1")


for i in predictors_need_norm:
    normalize_lag(data, i)

last_date = data.Date.max()
X = data[predictors]
print X.head()
y = data.target
X = X.replace([np.inf, -np.inf], 1) # replace inf as 1 for some bad data
X_oot = X[data.Date==last_date]
y_oot = y[data.Date==last_date]

X = X[data.Date < last_date]
y = y[data.Date < last_date]
X_training, X_test, y_training, y_test = train_test_split(X, y)


#rf = linear_model.LogisticRegression(C=1e5)
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_training, y_training)

y_oot_hat= rf.predict_proba(X_oot)
#metrics.confusion_matrix(y_oot, y_oot_hat)
y_and_yhat = pd.DataFrame({"y_oot":y_oot, "y_oot_hat":y_oot_hat[:,1]})
result = y_and_yhat.join(data, how='inner') 
result = result.sort(["y_oot_hat"], ascending=False)
print result.head(10)
print result.tail(10)


plt.scatter(y_oot_hat[:,1], data.increase_from_last_day[y_oot.index])
plt.show()