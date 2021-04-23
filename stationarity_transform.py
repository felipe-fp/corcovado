try:
    from statsmodels.tsa.stattools import adfuller
except ModuleNotFoundError:
    print('Module not found')

def stationarity_transform(series):
    p_value = adfuller(series)
    diff = 0
    while p_value <= 0.05:
        new_series = (series - series.shift(1)).dropna()
        p_value = adfuller(new_series)
        diff += 1
    return new_series, diff
