import pandas as pd

report_today = pd.read_csv("C:\Users\\ralph\OneDrive\Documents\GitHub\stocks_pred\stocks\\report_today.csv",
                           sep='\t')
SYMBOLS = list(report_today.iloc[:,0].apply(lambda x: x.split("_")[0]))
