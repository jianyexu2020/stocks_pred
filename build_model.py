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



import pandas as pd
data = pd.read_csv("stocks_with_lag_data.csv")
head(data)
data.head
data = pd.read_csv("stocks_with_lag_data.csv", sep=\t'')
data = pd.read_csv("stocks_with_lag_data.csv", sep='\t')
data.head
data.head()
data.shape
data.tail()
target = data.Adj_Close - data.Adj_Close_lag1
target.discribe()
target.describe()
target = (data.Adj_Close - data.Adj_Close_lag1) / data.Adj_Close_lag1
target.describe()
data.loc[target == -0.494230]
data.loc[target <= -0.494230]
datia.loc[target <= -0.494230]
datia.iloc[target <= -0.494230]
data.iloc[target <= -0.494230]
data.loc[target <= -0.494230]
target.describe()
from sklearn import RandomForest
from sklearn import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
target = (data.Adj_Close - data.Adj_Close_lag1) / data.Adj_Close_lag1 > 0
target.describe()
target.head()
int(target)
target.lambda(x: 1 if x is True else 0)
target.apply(lambda x: 1 if x is True else 0)
t = target.apply(lambda x: 1 if x is True else 0)
t.describe()
t.count()
t.unique()
t
t == 1
target > 1
target > 1
target.describe()
history
target = ((data.Adj_Close - data.Adj_Close_lag1) / data.Adj_Close_lag1) > 0
target.head()
target.value_count()
target.value_counts()
data.head()
data["ema_10"]
data.iloc[:, 10]
data.iloc[:, 16]
data.iloc[:, 17]
X = data.iloc[:, 17:]
X.head()
histroy
history
rf = RandomForestClassifier()
rf.fit(X, y)
rf.fit(X, target)
dir(rf)
rf.oob_score
rf.feature_importances_
X.columns
s = pd.DataFrame(rf.feature_importances_, X.columns)
s
X.delete("target")
delect X["target"]
delete X["target"]
X.columns
X.target
delete X["target"]
del X["target"]
del X["increase_from_last_day"]
rf = RandomForestClassifier(oob_score = True)
rf.fit(X, y)
rf.fit(X, target)
rf.fit(X, target)
rf.fit(X, target)
X.shape
target.shape
rf.fit(X.iloc[:20000,:], target[:20000])
dir(rf)
rf.oob_score_
rf.oob_score
rf.predict(X[20000:])
rf.predict(X[20000:40000])
rf.predict_proba(X[20000:40000])
p = rf.predict_proba(X[20000:40000])
pd.DataFrame(target[20000:40000], p[:,1])
p[:,1]
p[:,0]
pd.DataFrame(target[20000:40000], p[:,1])
target[20000:40000]
target.value_counts()
target = target.apply(lambda x: 1 if x is True else 0)
pd.DataFrame(target[20000:40000], p[:,1])
target
pd.DataFrame(np.array(target[20000:40000]), p[:,1])
import numpy as np
pd.DataFrame(np.array(target[20000:40000]), p[:,1])
target[20000:40000].value_counts()
target.value_counts()
history
target = ((data.Adj_Close - data.Adj_Close_lag1) / data.Adj_Close_lag1) > 0
target.value_counts()
type(target)
int(target)
np.array(target)
s = target.apply(lambda x: 1 if x is True else 0)
s.value_counts()
np.array(target) * 1
target = target * 1
target
hisotry
history
pd.DataFrame(np.array(target[20000:40000]), p[:,1])
s = pd.DataFrame(np.array(target[20000:40000]), p[:,1])
type(s)
s.head()
s.sort()
s.sort(ascending=False)
X.head()
X.shape()
X.shape
X.columns
history



