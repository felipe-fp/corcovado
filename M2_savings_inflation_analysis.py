import pandas as pd
import matplotlib.pyplot as plt

inflation = pd.read_csv('Price_index.csv',index_col = 0)

inflation.columns = ['price']
inflation['delta'] = ((inflation['price'] - inflation['price'].shift(12))/inflation['price']) * 100

#plt.figure(1)
#inflation['delta'].plot()
#plt.show()

m2 = pd.read_csv('M2_USA.csv', index_col = 0)
m2.columns = ['M2']
m2['M2'] = m2['M2'] / 1000000000

savings = pd.read_csv('SAVINGSL.csv', index_col = 0)
savings.columns = ['Savings']

donnee = m2['M2']/savings['Savings']

# print(donnee)

# plt.figure(1)
# inflation['delta'].plot()
# donnee.plot()
# plt.show()



## Felipe
import numpy as np
donnee_MA = donnee.rolling(12).mean().dropna()
donnee_MA = pd.DataFrame(donnee_MA)
donnee_MA.columns = ['MA(12) M2/savings']

infl_MA = inflation['delta'].rolling(12).mean().dropna()
infl_MA = pd.DataFrame(infl_MA)
infl_MA.columns = ['MA(12) inflation']

MA_graph_df = donnee_MA.join(infl_MA)

# plt.figure(1)
# MA_graph_df.plot()
# plt.legend()
# plt.show()

x = donnee.loc['1985-01-01':'2017-03-01'].values
x = x.reshape(1, x.shape[0])[0]
x_index = np.arange(0, x.shape[0])
y = inflation.loc['1985-01-01':'2017-03-01']['delta'].values
y = y.reshape(1, y.shape[0])[0]
y_index = np.arange(0, y.shape[0])

from scipy import stats
slope_x, intercept_x, r_value_x, p_value_x, std_err_x = stats.linregress(x_index, x)
slope_y, intercept_y, r_value_y, p_value_y, std_err_y = stats.linregress(y_index, y)

x_hat = x_index * slope_x + intercept_x
y_hat = y_index * slope_y + intercept_y

plt.figure(1)
plt.plot(x, label = 'M2/savings')
plt.plot(x_hat, label = 'M2/savings linereg')
plt.plot(y, label = 'inflation')
plt.plot(y_hat, label = 'M2/savings linreg')
plt.legend()
plt.show()

slope_, intercept_, r_value_, p_value_, std_err_ = stats.linregress(x, y)
print('Slope is equal to ',slope_, 'and p_value is equal to', p_value_)

plt.figure(1)
y_ = slope_ * x + intercept_
plt.plot(y_)
plt.plot(y)
plt.show()



