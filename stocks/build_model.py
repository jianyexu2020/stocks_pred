#!/usr/bin/python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import matplotlib.pyplot as plt


def build_model():
    pd.set_option('display.max_columns', 30)
    def normalize_lag(df, lag_col):
        if "v_" in lag_col:
            df[lag_col] =  df[lag_col] / df['Volume_lag1']
        elif "cv_" in lag_col:
            df[lag_col] = df[lag_col] / df['Adj_Close_Volume_lag1']
        elif "rolling" in lag_col or "ema" in lag_col:
            df[lag_col] = df[lag_col] / df['Adj_Close_lag1']

    data = pd.read_csv(
        "C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\stocks\stocks_with_lag_data.csv",
        sep='\t')
    predictors = [x for x in data.columns if "lag" in x]

    for i in predictors:
        normalize_lag(data, i)

    last_date = data.Date.max()
    X = data[predictors]
    print X.head()
    y = data.increase_from_last_day
    X = X.fillna(-1) # replace inf as 1 for some bad data
    X = np.round(X, 2)
    X_oot = X[data.Date==last_date]
    y_oot = y[data.Date==last_date]

    X = X[data.Date < last_date]
    y = y[data.Date < last_date]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=2828)



    #rf = linear_model.LogisticRegression(C=1e5)
    rf = RandomForestRegressor(n_estimators=100, n_jobs=4)
    print "Start fitting model..."
    rf.fit(X_train, y_train)
    with open("rf.pk", "wb") as f:
        pickle.dump(rf, f)
    y_oot_hat= rf.predict(X_oot)
    #metrics.confusion_matrix(y_oot, y_oot_hat)
    y_and_yhat = pd.DataFrame({"y_oot":y_oot, "y_oot_hat":y_oot_hat})
    result = y_and_yhat.join(data, how='inner')
    result = result.sort_values(by="y_oot_hat", ascending=False)
    print result.head(10)
    print result.tail(10)

    plt.scatter(y_oot_hat, y_oot)
    plt.show()
    return rf

if __name__ == "__main__":
    build_model()