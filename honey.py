import seaborn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

df = pd.read_csv(r"honeyproduction.csv")

prod_per_year = df.groupby('year').totalprod.mean().reset_index()

x = prod_per_year["year"]
x = x.values.reshape(-1, 1)

y = prod_per_year["totalprod"]

plt.scatter(x, y)

regr = linear_model.LinearRegression()
regr.fit(x, y)

#The slope of the line will be the first (and only) element of the regr.coef_
print(regr.coef_[0])

y_pred = regr.predict(x)

x_future = np.array(range(2013, 2018))
x_future = x_future.reshape(-1, 1)

future = regr.predict(x_future)
plt.plot(x, y_pred)
plt.plot(x_future, future)
plt.show()