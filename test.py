import pandas as pd
import numpy as np

dframe = pd.read_csv("C:/Users/George/Documents/.Projects/quantium-govhack-2023/finaldata.csv")
dframe.head()

from statsmodels.formula.api import logit
logistic = logit("Total.Score ~ Rural", 
                 data = dframe).fit()
print(logistic)




















